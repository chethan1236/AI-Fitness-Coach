"""Progress tracking API endpoints."""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.v1.dependencies import CurrentUser
from app.database.dependencies import DatabaseSession
from app.repositories.progress_repository import ProgressRepository
from app.schemas.progress import (
    ProgressAnalysisRequest,
    ProgressAnalysisResponse,
    ProgressCreateRequest,
    ProgressResponse,
)
from app.services.progress_ai_service import ProgressAIService
from app.utils.body_metrics import calculate_bmi, calculate_body_fat_percentage
from app.models.progress_log import ProgressLog

router = APIRouter()


@router.post("/", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
def create_progress(
    payload: ProgressCreateRequest,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> ProgressResponse:
    bmi = calculate_bmi(payload.weight, current_user.height or 0)
    body_fat_percentage = calculate_body_fat_percentage(bmi, current_user.age, current_user.gender)

    progress_log = ProgressLog(
        user_id=current_user.id,
        weight=payload.weight,
        waist=payload.waist,
        bmi=bmi,
        body_fat_percentage=body_fat_percentage,
        notes=payload.notes,
    )

    ProgressRepository(session).create(progress_log)
    session.commit()
    session.refresh(progress_log)
    return progress_log


@router.get("/", response_model=list[ProgressResponse])
def list_progress(current_user: CurrentUser, session: DatabaseSession) -> list[ProgressResponse]:
    return ProgressRepository(session).list_by_user(current_user.id)


@router.get("/latest", response_model=ProgressResponse)
def get_latest_progress(current_user: CurrentUser, session: DatabaseSession) -> ProgressResponse:
    progress_log = ProgressRepository(session).get_latest_by_user(current_user.id)
    if progress_log is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No progress logs found")
    return progress_log


@router.get("/{progress_id}", response_model=ProgressResponse)
def get_progress(progress_id: UUID, current_user: CurrentUser, session: DatabaseSession) -> ProgressResponse:
    progress_log = ProgressRepository(session).get_by_id(progress_id)
    if progress_log is None or progress_log.user_id != current_user.id:
        from fastapi import HTTPException

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress log not found")
    return progress_log


@router.post("/analyze", response_model=ProgressAnalysisResponse)
def analyze_progress(
    payload: ProgressAnalysisRequest,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> ProgressAnalysisResponse:
    analysis = ProgressAIService(session).analyze_progress(current_user, payload)
    return ProgressAnalysisResponse(**analysis)
