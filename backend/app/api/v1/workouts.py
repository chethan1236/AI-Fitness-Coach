"""Workout generation API endpoints."""

from fastapi import APIRouter, status

from app.api.v1.dependencies import CurrentUser
from app.database.dependencies import DatabaseSession
from app.schemas.workout import WorkoutGenerateRequest, WorkoutPlanResponse
from app.services.workout_ai_service import WorkoutAIService

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/generate", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
def generate_workout(
    payload: WorkoutGenerateRequest,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> WorkoutPlanResponse:
    workout_plan = WorkoutAIService(session).generate_workout_plan(current_user, payload)
    return workout_plan
