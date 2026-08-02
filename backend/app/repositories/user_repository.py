"""Persistence operations for users and refresh tokens."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import RefreshToken, User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email.lower()))

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)

    def create_user(self, user: User) -> User:
        self.session.add(user)
        return user

    def add_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.session.add(refresh_token)
        return refresh_token

    def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        return self.session.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))

    def revoke_refresh_token(self, refresh_token: RefreshToken) -> None:
        if refresh_token.revoked_at is None:
            refresh_token.revoked_at = datetime.now(UTC)
