"""Authentication use cases and token-rotation policy."""

from uuid import UUID

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    fingerprint_token,
    hash_password,
    verify_password,
)
from app.models.user import RefreshToken, User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenPair, UserRegistration

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password",
    headers={"WWW-Authenticate": "Bearer"},
)
INVALID_REFRESH_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired refresh token",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.users = UserRepository(session)

    def register(self, payload: UserRegistration) -> User:
        if self.users.get_by_email(str(payload.email)):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

        user = User(
            name=payload.name.strip(), email=str(payload.email).lower(), password_hash=hash_password(payload.password),
            age=payload.age, gender=payload.gender, height=payload.height, weight=payload.weight,
            goal=payload.goal, experience=payload.experience,
        )
        self.users.create_user(user)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered") from None
        self.session.refresh(user)
        return user

    def authenticate(self, payload: LoginRequest) -> TokenPair:
        user = self.users.get_by_email(str(payload.email))
        if user is None or not verify_password(payload.password, user.password_hash):
            raise INVALID_CREDENTIALS
        return self._issue_token_pair(user)

    def refresh(self, raw_refresh_token: str) -> TokenPair:
        refresh_token = self._validate_refresh_token(raw_refresh_token)
        self.users.revoke_refresh_token(refresh_token)
        return self._issue_token_pair(refresh_token.user)

    def logout(self, raw_refresh_token: str, current_user_id: UUID) -> None:
        refresh_token = self._validate_refresh_token(raw_refresh_token)
        if refresh_token.user_id != current_user_id:
            raise INVALID_REFRESH_TOKEN
        self.users.revoke_refresh_token(refresh_token)
        self.session.commit()

    def _issue_token_pair(self, user: User) -> TokenPair:
        access_token = create_access_token(str(user.id))
        raw_refresh_token, expires_at = create_refresh_token(str(user.id))
        self.users.add_refresh_token(
            RefreshToken(user_id=user.id, token_hash=fingerprint_token(raw_refresh_token), expires_at=expires_at)
        )
        self.session.commit()
        return TokenPair(access_token=access_token, refresh_token=raw_refresh_token)

    def _validate_refresh_token(self, raw_token: str) -> RefreshToken:
        try:
            payload = decode_access_token(raw_token)
            if payload.get("type") != "refresh" or not payload.get("sub"):
                raise INVALID_REFRESH_TOKEN
        except JWTError:
            raise INVALID_REFRESH_TOKEN from None

        refresh_token = self.users.get_refresh_token(fingerprint_token(raw_token))
        if refresh_token is None or refresh_token.revoked_at is not None:
            raise INVALID_REFRESH_TOKEN
        return refresh_token
