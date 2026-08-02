"""Pydantic schemas for workout generation and plan delivery."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkoutGenerateRequest(BaseModel):
    goal_override: str | None = None


class WorkoutPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    plan_json: dict[str, Any]
