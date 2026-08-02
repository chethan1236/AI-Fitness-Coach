"""Persistence operations for progress logs."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.progress_log import ProgressLog


class ProgressRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, progress_log: ProgressLog) -> ProgressLog:
        self.session.add(progress_log)
        return progress_log

    def get_by_id(self, progress_id: UUID) -> ProgressLog | None:
        return self.session.get(ProgressLog, progress_id)

    def list_by_user(self, user_id: UUID) -> list[ProgressLog]:
        statement = select(ProgressLog).where(ProgressLog.user_id == user_id).order_by(ProgressLog.created_at.desc())
        return self.session.scalars(statement).all()

    def get_latest_by_user(self, user_id: UUID) -> ProgressLog | None:
        statement = select(ProgressLog).where(ProgressLog.user_id == user_id).order_by(ProgressLog.created_at.desc())
        return self.session.scalar(statement)
