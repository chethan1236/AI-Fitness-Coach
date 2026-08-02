"""Pydantic schemas for progress tracking and analysis."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProgressCreateRequest(BaseModel):
    weight: float = Field(..., gt=0, description="Current body weight in kg")
    waist: float = Field(..., gt=0, description="Current waist measurement in cm")
    notes: str | None = Field(default=None, description="Optional progress notes")


class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    weight: float
    waist: float
    bmi: float
    body_fat_percentage: float
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class ProgressAnalysisRequest(BaseModel):
    notes: str | None = None


class ProgressAnalysisResponse(BaseModel):
    feedback: str
    recommendations: list[str]
    summary: str
    original_notes: str | None = None
    progress: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)