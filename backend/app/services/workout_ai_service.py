"""AI-powered workout generation service."""

import json
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import google.generativeai as genai

from app.core.config import settings
from app.models.user import User
from app.models.workout_plan import WorkoutPlan
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.workout import WorkoutGenerateRequest


class WorkoutAIService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = WorkoutRepository(session)
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key is not configured",
            )
        genai.configure(api_key=settings.gemini_api_key)

    def generate_workout_plan(self, user: User, payload: WorkoutGenerateRequest) -> WorkoutPlan:
        plan_data = self._call_gemini(user, payload)

        if not isinstance(plan_data, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected response format from AI workout generator",
            )

        title = plan_data.get("title")
        if not title or not isinstance(title, str):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI generated workout plan is missing a title",
            )

        workout_plan = WorkoutPlan(user_id=user.id, title=title, plan_json=plan_data)
        self.repository.create(workout_plan)
        self.session.commit()
        self.session.refresh(workout_plan)
        return workout_plan

    def _call_gemini(self, user: User, payload: WorkoutGenerateRequest) -> dict[str, Any]:
        prompt = self._build_prompt(user, payload)

        model = genai.GenerativeModel("gemini-3.6-flash")

        response = model.generate_content(prompt)

        text = self._extract_text(response)

        return self._parse_json(text)

    def _resolve_model_name(self) -> str:
        models = genai.list_models()
        for model in models:
            supported_methods = getattr(model, "supported_generation_methods", None)
            if supported_methods is None:
                supported_methods = getattr(model, "supported_generation_models", None)
            if supported_methods and "generateContent" in supported_methods:
                return getattr(model, "name", None) or getattr(model, "id", None)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No available Gemini models support generateContent.",
        )

    def _build_prompt(self, user: User, payload: WorkoutGenerateRequest) -> str:
        goal = payload.goal_override or user.goal or "general fitness"
        workout_days = user.workout_days if user.workout_days is not None else 3
        experience = user.experience or "beginner"
        preferred_time = user.preferred_workout_time or "not specified"
        gender = user.gender or "not specified"
        age = str(user.age) if user.age is not None else "not specified"
        height = str(user.height) if user.height is not None else "not specified"
        weight = str(user.weight) if user.weight is not None else "not specified"

        return (
            "Generate a personalized workout plan in valid JSON only. "
            "Do not include any explanation, markdown, or text outside the JSON object. "
            "Use the exact structure shown below."
            "\n\n"
            "Expected JSON structure:\n"
            "{\n"
            "  \"title\": \"\",\n"
            "  \"days\": [\n"
            "    {\n"
            "      \"day\": \"\",\n"
            "      \"muscle_group\": \"\",\n"
            "      \"exercises\": [\n"
            "        {\n"
            "          \"name\": \"\",\n"
            "          \"sets\": 4,\n"
            "          \"reps\": \"10-12\"\n"
            "        }\n"
            "      ]\n"
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
            f"- preferred_workout_time: {preferred_time}\n\n"
            "Create a workout plan that matches the provided profile. "
            "Return only valid JSON with title and days as shown above."
        )

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
                detail="AI workout generator returned an empty response.",
            )

        json_text = self._extract_json_object(text)
        try:
            parsed = json.loads(json_text)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI workout generator returned invalid JSON.",
            ) from exc

        if not isinstance(parsed, dict):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI workout generator returned JSON in the wrong format.",
            )

        return parsed

    def _extract_json_object(self, text: str) -> str:
        start = text.find("{")
        if start == -1:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI workout generator response did not contain JSON.",
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
            detail="AI workout generator returned malformed JSON.",
        )
