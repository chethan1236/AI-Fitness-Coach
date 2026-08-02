"""AI-powered progress analysis service."""

import json
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import google.generativeai as genai

from app.core.config import settings
from app.models.user import User
from app.repositories.progress_repository import ProgressRepository
from app.schemas.progress import ProgressAnalysisRequest


class ProgressAIService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = ProgressRepository(session)
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key is not configured",
            )
        genai.configure(api_key=settings.gemini_api_key)

    def analyze_progress(self, user: User, payload: ProgressAnalysisRequest) -> dict[str, Any]:
        prompt = self._build_prompt(user, payload)
        model = genai.GenerativeModel(settings.gemini_model)
        try:
            response = model.generate_content(prompt)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate progress feedback from Gemini.",
            ) from exc

        text = self._extract_text(response)
        return self._parse_json(text)

    def _build_prompt(self, user: User, payload: ProgressAnalysisRequest) -> str:
        gender = user.gender or "not specified"
        age = str(user.age) if user.age is not None else "not specified"
        height = str(user.height) if user.height is not None else "not specified"
        weight = str(user.weight) if user.weight is not None else "not specified"
        goal = user.goal or "general fitness"
        experience = user.experience or "beginner"
        workout_days = user.workout_days if user.workout_days is not None else 3
        preferred_time = user.preferred_workout_time or "not specified"
        diet_preference = user.diet_preference or "not specified"
        calories = str(user.daily_calorie_goal) if user.daily_calorie_goal is not None else "not specified"
        notes = payload.notes or ""

        return (
            "Provide personalized progress feedback in valid JSON only. "
            "Do not include any explanation, markdown, or text outside the JSON object. "
            "Use the exact structure shown below."
            "\n\n"
            "Expected JSON structure:\n"
            "{\n"
            "  \"feedback\": \"\",\n"
            "  \"recommendations\": [\n"
            "    \"...\"\n"
            "  ],\n"
            "  \"summary\": \"\",\n"
            "  \"original_notes\": \"\",\n"
            "  \"progress\": {\n"
            "    \"weight\": 0,\n"
            "    \"waist\": 0,\n"
            "    \"bmi\": 0,\n"
            "    \"body_fat_percentage\": 0\n"
            "  }\n"
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
            f"- daily_calorie_goal: {calories}\n"
            f"- notes: {notes}\n\n"
            "Return only valid JSON with feedback, recommendations, summary, original_notes, and progress metrics."
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
                detail="AI progress analysis returned an empty response.",
            )

        json_text = self._extract_json_object(text)
        try:
            parsed = json.loads(json_text)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI progress analysis returned invalid JSON.",
            ) from exc

        if not isinstance(parsed, dict):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI progress analysis returned JSON in the wrong format.",
            )

        return parsed

    def _extract_json_object(self, text: str) -> str:
        start = text.find("{")
        if start == -1:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI progress analysis response did not contain JSON.",
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
            detail="AI progress analysis returned malformed JSON.",
        )
