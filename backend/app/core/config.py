"""Convenient access point for application configuration."""

from app.core.settings import Settings, get_settings

settings: Settings = get_settings()
