"""Pydantic schemas for chat endpoints."""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    message: str
    response: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ChatMessageResponse]
