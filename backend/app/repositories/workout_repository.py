"""Persistence operations for workout plans."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workout_plan import WorkoutPlan


class WorkoutRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        self.session.add(workout_plan)
        return workout_plan

    def get_latest_by_user(self, user_id: UUID) -> WorkoutPlan | None:
        statement = select(WorkoutPlan).where(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.created_at.desc())
        return self.session.scalar(statement)
