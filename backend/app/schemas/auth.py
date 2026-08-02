"""Pydantic contracts for authentication and user profile APIs."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Gender(StrEnum):
    male = "male"
    female = "female"
    non_binary = "non_binary"
    prefer_not_to_say = "prefer_not_to_say"


class FitnessGoal(StrEnum):
    lose_weight = "lose_weight"
    build_muscle = "build_muscle"
    improve_fitness = "improve_fitness"
    maintain_health = "maintain_health"


class ExperienceLevel(StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class PreferredWorkoutTime(StrEnum):
    morning = "morning"
    afternoon = "afternoon"
    evening = "evening"
    night = "night"


class DietPreference(StrEnum):
    balanced = "balanced"
    low_carb = "low_carb"
    high_protein = "high_protein"
    vegetarian = "vegetarian"
    vegan = "vegan"
    paleo = "paleo"
    keto = "keto"


class UserRegistration(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    age: int | None = Field(default=None, ge=13, le=120)
    gender: Gender | None = None
    height: float | None = Field(default=None, gt=0, le=300)
    weight: float | None = Field(default=None, gt=0, le=700)
    goal: FitnessGoal | None = None
    experience: ExperienceLevel | None = None


class ProfileUpdateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int | None = Field(default=None, ge=13, le=120)
    gender: Gender | None = None
    height: float | None = Field(default=None, gt=0, le=300)
    weight: float | None = Field(default=None, gt=0, le=700)
    goal: FitnessGoal | None = None
    experience: ExperienceLevel | None = None
    workout_days: int | None = Field(default=None, ge=0, le=7)
    preferred_workout_time: PreferredWorkoutTime | None = None
    diet_preference: DietPreference | None = None
    daily_calorie_goal: int | None = Field(default=None, ge=0)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1)


class LogoutRequest(RefreshRequest):
    pass


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    age: int | None
    gender: Gender | None
    height: float | None
    weight: float | None
    goal: FitnessGoal | None
    experience: ExperienceLevel | None
    created_at: datetime
    workout_days: int | None
    preferred_workout_time: PreferredWorkoutTime | None
    diet_preference: DietPreference | None
    daily_calorie_goal: int | None
    updated_at: datetime


class MessageResponse(BaseModel):
    message: str
