"""Diet generation API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.v1.dependencies import CurrentUser
from app.database.dependencies import DatabaseSession
from app.repositories.diet_repository import DietRepository
from app.schemas.diet import DietGenerateRequest, DietPlanResponse
from app.services.diet_ai_service import DietAIService

router = APIRouter()


@router.post("/generate", response_model=DietPlanResponse, status_code=status.HTTP_201_CREATED)
def generate_diet(
    payload: DietGenerateRequest,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> DietPlanResponse:
    diet_plan = DietAIService(session).generate_diet_plan(current_user, payload)
    return diet_plan


@router.get("/", response_model=list[DietPlanResponse])
def list_diets(current_user: CurrentUser, session: DatabaseSession) -> list[DietPlanResponse]:
    diet_plans = DietRepository(session).list_by_user(current_user.id)
    return diet_plans


@router.get("/{diet_id}", response_model=DietPlanResponse)
def get_diet(diet_id: UUID, current_user: CurrentUser, session: DatabaseSession) -> DietPlanResponse:
    diet_plan = DietRepository(session).get_by_id(diet_id)
    if diet_plan is None or diet_plan.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diet plan not found")
    return diet_plan
