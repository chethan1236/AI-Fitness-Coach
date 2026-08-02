"""Pydantic schemas for diet generation and diet plans."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DietGenerateRequest(BaseModel):
    goal_override: str | None = None


class DietPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    plan_json: dict[str, Any]
