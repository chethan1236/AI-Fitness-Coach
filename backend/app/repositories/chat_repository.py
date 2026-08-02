"""Persistence operations for chat history."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory


class ChatRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, chat: ChatHistory) -> ChatHistory:
        self.session.add(chat)
        return chat

    def list_by_user(self, user_id: UUID) -> list[ChatHistory]:
        statement = select(ChatHistory).where(ChatHistory.user_id == user_id).order_by(ChatHistory.created_at.desc())
        return self.session.scalars(statement).all()

    def delete_all_for_user(self, user_id: UUID) -> int:
        stmt = delete(ChatHistory).where(ChatHistory.user_id == user_id)
        result = self.session.execute(stmt)
        return result.rowcount
