from fastapi import APIRouter, status

from app.api.v1.dependencies import CurrentUser
from app.database.dependencies import DatabaseSession
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    MessageResponse,
    RefreshRequest,
    TokenPair,
    UserRegistration,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegistration, session: DatabaseSession) -> UserResponse:
    return AuthService(session).register(payload)


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, session: DatabaseSession) -> TokenPair:
    return AuthService(session).authenticate(payload)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, session: DatabaseSession) -> TokenPair:
    return AuthService(session).refresh(payload.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(payload: LogoutRequest, current_user: CurrentUser, session: DatabaseSession) -> MessageResponse:
    AuthService(session).logout(payload.refresh_token, current_user.id)
    return MessageResponse(message="Successfully logged out")
