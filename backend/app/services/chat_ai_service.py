"""AI chat service integrating user context with Gemini."""

import json
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import google.generativeai as genai

from app.core.config import settings
from app.models.chat_history import ChatHistory
from app.models.user import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.workout_repository import WorkoutRepository
from app.repositories.diet_repository import DietRepository
from app.repositories.progress_repository import ProgressRepository
from app.schemas.chat import ChatRequest


class ChatAIService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = ChatRepository(session)
        if not settings.gemini_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key is not configured",
            )
        genai.configure(api_key=settings.gemini_api_key)

    def chat(self, user: User, payload: ChatRequest) -> ChatHistory:
        # Gather context
        workout = WorkoutRepository(self.session).get_latest_by_user(user.id)
        diet = DietRepository(self.session).get_by_id(WorkoutRepository) if False else DietRepository(self.session).list_by_user(user.id)[:1]
        # above line uses list_by_user to fetch latest diet if available
        latest_diet = diet[0] if diet else None
        progress = ProgressRepository(self.session).get_latest_by_user(user.id)

        prompt = self._build_prompt(user, payload.message, workout, latest_diet, progress)

        model = genai.GenerativeModel(settings.gemini_model)
        try:
            response = model.generate_content(prompt)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate chat response from Gemini.",
            ) from exc

        text = self._extract_text(response)

        # Save chat history
        chat = ChatHistory(user_id=user.id, message=payload.message, response=text)
        self.repository.create(chat)
        self.session.commit()
        self.session.refresh(chat)
        return chat

    def _build_prompt(self, user: User, message: str, workout, diet, progress) -> str:
        lines = [
            "You are an AI fitness coach assistant. Use the user's context below to respond helpfully.",
            "Return only the assistant's response as plain text (no markdown, no JSON wrapper).",
            "\nUser profile:",
            f"- name: {getattr(user, 'name', 'N/A')}",
            f"- age: {getattr(user, 'age', 'N/A')}",
            f"- gender: {getattr(user, 'gender', 'N/A')}",
            f"- height: {getattr(user, 'height', 'N/A')}",
            f"- weight: {getattr(user, 'weight', 'N/A')}",
            f"- goal: {getattr(user, 'goal', 'N/A')}",
            f"- experience: {getattr(user, 'experience', 'N/A')}",
            f"- workout_days: {getattr(user, 'workout_days', 'N/A')}",
            f"- preferred_workout_time: {getattr(user, 'preferred_workout_time', 'N/A')}",
            f"- diet_preference: {getattr(user, 'diet_preference', 'N/A')}",
            f"- daily_calorie_goal: {getattr(user, 'daily_calorie_goal', 'N/A')}",
        ]

        if workout:
            lines.append("\nLatest workout plan:")
            lines.append(json.dumps(workout.plan_json))

        if diet:
            lines.append("\nLatest diet plan:")
            if latest_diet := (diet[0] if isinstance(diet, list) and diet else diet):
                lines.append(json.dumps(latest_diet.plan_json))

        if progress:
            lines.append("\nLatest progress:")
            progress_data = {
                "weight": getattr(progress, "weight", None),
                "waist": getattr(progress, "waist", None),
                "bmi": getattr(progress, "bmi", None),
                "body_fat_percentage": getattr(progress, "body_fat_percentage", None),
            }
            lines.append(json.dumps(progress_data))

        lines.append("\nUser message:")
        lines.append(message)

        return "\n".join(lines)

    def _extract_text(self, response: Any) -> str:
        if response is None:
            return ""

        if hasattr(response, "text") and isinstance(response.text, str):
            return response.text
        if isinstance(response, dict) and isinstance(response.get("text"), str):
            return response["text"]
        if hasattr(response, "response") and hasattr(response.response, "text"):
            return response.response.text
        return str(response)
