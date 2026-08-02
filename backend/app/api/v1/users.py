from fastapi import APIRouter, status

from app.api.v1.dependencies import CurrentUser
from app.database.dependencies import DatabaseSession
from app.schemas.auth import ProfileUpdateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser) -> UserResponse:
    return current_user


@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_me(payload: ProfileUpdateRequest, current_user: CurrentUser, session: DatabaseSession) -> UserResponse:
    current_user.name = payload.name.strip()
    current_user.age = payload.age
    current_user.gender = payload.gender
    current_user.height = payload.height
    current_user.weight = payload.weight
    current_user.goal = payload.goal
    current_user.experience = payload.experience
    current_user.workout_days = payload.workout_days
    current_user.preferred_workout_time = payload.preferred_workout_time
    current_user.diet_preference = payload.diet_preference
    current_user.daily_calorie_goal = payload.daily_calorie_goal
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
