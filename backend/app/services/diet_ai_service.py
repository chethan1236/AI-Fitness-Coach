"""AI-powered diet generation service."""

import json
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import google.generativeai as genai

from app.core.config import settings
from app.models.diet_plan import DietPlan
from app.models.user import User
from app.repositories.diet_repository import DietRepository
from app.schemas.diet import DietGenerateRequest


class DietAIService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = DietRepository(session)
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key is not configured",
            )
        genai.configure(api_key=settings.gemini_api_key)

    def generate_diet_plan(self, user: User, payload: DietGenerateRequest) -> DietPlan:
        plan_data = self._call_gemini(user, payload)

        if not isinstance(plan_data, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected response format from AI diet generator",
            )

        title = plan_data.get("title")
        if not title or not isinstance(title, str):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI generated diet plan is missing a title",
            )

        diet_plan = DietPlan(user_id=user.id, title=title, plan_json=plan_data)
        self.repository.create(diet_plan)
        self.session.commit()
        self.session.refresh(diet_plan)
        return diet_plan

    def _call_gemini(self, user: User, payload: DietGenerateRequest) -> dict[str, Any]:
        prompt = self._build_prompt(user, payload)
        model = genai.GenerativeModel(settings.gemini_model)
        try:
            response = model.generate_content(prompt)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate diet plan from Gemini.",
            ) from exc

        text = self._extract_text(response)
        return self._parse_json(text)

    def _build_prompt(self, user: User, payload: DietGenerateRequest) -> str:
        goal = payload.goal_override or user.goal or "general health"
        workout_days = user.workout_days if user.workout_days is not None else 3
        experience = user.experience or "beginner"
        preferred_time = user.preferred_workout_time or "not specified"
        diet_preference = user.diet_preference or "balanced"
        calories = user.daily_calorie_goal or self._estimate_calories(user)
        gender = user.gender or "not specified"
        age = str(user.age) if user.age is not None else "not specified"
        height = str(user.height) if user.height is not None else "not specified"
        weight = str(user.weight) if user.weight is not None else "not specified"

        return (
            "Generate a personalized diet plan in valid JSON only. "
            "Do not include any explanation, markdown, or text outside the JSON object. "
            "Use the exact structure shown below."
            "\n\n"
            "Expected JSON structure:\n"
            "{\n"
            "  \"title\": \"\",\n"
            "  \"total_calories\": 2200,\n"
            "  \"protein\": \"140g\",\n"
            "  \"carbs\": \"220g\",\n"
            "  \"fat\": \"60g\",\n"
            "  \"water\": \"3.5L\",\n"
            "  \"meals\": [\n"
            "    {\n"
            "      \"meal\": \"Breakfast\",\n"
            "      \"time\": \"8:00 AM\",\n"
            "      \"foods\": [\n"
            "        \"80g Oats\",\n"
            "        \"250ml Milk\",\n"
            "        \"2 Eggs\"\n"
            "      ],\n"
            "      \"calories\": 500\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            "User profile:\n"
            f"- age: {age}\n"
            f"- gender: {gender}\n"
            f"- height: {height}\n"
            f"- weight: {weight}\n"
            f"- goal: {goal}\n"
            f"- experience: {experience}\n"
            f"- workout_days: {workout_days}\n"
            f"- preferred_workout_time: {preferred_time}\n"
            f"- diet_preference: {diet_preference}\n"
            f"- daily_calorie_goal: {calories}\n\n"
            "Create a diet plan that matches the provided profile. "
            "Return only valid JSON with title, total_calories, macros, water, and meals."
        )

    def _estimate_calories(self, user: User) -> int:
        if user.age is None or user.height is None or user.weight is None:
            return 2000
        base = 10 * float(user.weight) + 6.25 * float(user.height) - 5 * float(user.age)
        if user.gender == "male":
            base += 5
        elif user.gender == "female":
            base -= 161
        return int(base * 1.4)

    def _extract_text(self, response: Any) -> str:
        if response is None:
            return ""

        text = ""
        if hasattr(response, "text") and isinstance(response.text, str):
            text = response.text
        elif isinstance(response, dict) and isinstance(response.get("text"), str):
            text = response["text"]
        elif hasattr(response, "response") and hasattr(response.response, "text"):
            text = response.response.text
        else:
            text = str(response)

        return self._strip_code_fences(text)

    def _strip_code_fences(self, text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("```json") and stripped.endswith("```"):
            return stripped[len("```json"):-3].strip()
        if stripped.startswith("```") and stripped.endswith("```"):
            return stripped[3:-3].strip()
        return stripped

    def _parse_json(self, text: str) -> dict[str, Any]:
        if not text:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI diet generator returned an empty response.",
            )

        json_text = self._extract_json_object(text)
        try:
            parsed = json.loads(json_text)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI diet generator returned invalid JSON.",
            ) from exc

        if not isinstance(parsed, dict):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI diet generator returned JSON in the wrong format.",
            )

        return parsed

    def _extract_json_object(self, text: str) -> str:
        start = text.find("{")
        if start == -1:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI diet generator response did not contain JSON.",
            )

        depth = 0
        in_string = False
        escaped = False

        for index, char in enumerate(text[start:], start=start):
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI diet generator returned malformed JSON.",
        )
