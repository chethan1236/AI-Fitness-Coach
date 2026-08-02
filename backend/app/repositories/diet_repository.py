"""Persistence operations for diet plans."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.diet_plan import DietPlan


class DietRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, diet_plan: DietPlan) -> DietPlan:
        self.session.add(diet_plan)
        return diet_plan

    def get_by_id(self, diet_id: UUID) -> DietPlan | None:
        return self.session.get(DietPlan, diet_id)

    def list_by_user(self, user_id: UUID) -> list[DietPlan]:
        statement = select(DietPlan).where(DietPlan.user_id == user_id).order_by(DietPlan.created_at.desc())
        return self.session.scalars(statement).all()
