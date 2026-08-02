"""Chat API endpoints for user-AI conversation."""

from fastapi import APIRouter, status

from app.api.v1.dependencies import CurrentUser
from app.database.dependencies import DatabaseSession
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest, ChatMessageResponse
from app.services.chat_ai_service import ChatAIService

router = APIRouter()


@router.post("/", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(payload: ChatRequest, current_user: CurrentUser, session: DatabaseSession) -> ChatMessageResponse:
    chat = ChatAIService(session).chat(current_user, payload)
    return chat


@router.get("/history", response_model=list[ChatMessageResponse])
def get_history(current_user: CurrentUser, session: DatabaseSession) -> list[ChatMessageResponse]:
    return ChatRepository(session).list_by_user(current_user.id)


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
def clear_history(current_user: CurrentUser, session: DatabaseSession):
    ChatRepository(session).delete_all_for_user(current_user.id)
    session.commit()
    return None
