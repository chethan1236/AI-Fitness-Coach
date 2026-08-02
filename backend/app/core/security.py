"""Reusable security primitives for the future authentication module."""

import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def _create_token(subject: str, token_type: str, expires_delta: timedelta) -> tuple[str, datetime]:
    expires_at = datetime.now(UTC) + expires_delta
    payload = {"sub": subject, "type": token_type, "jti": str(uuid.uuid4()), "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm), expires_at


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    token, _ = _create_token(
        subject,
        "access",
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes),
    )
    return token


def create_refresh_token(subject: str) -> tuple[str, datetime]:
    return _create_token(subject, "refresh", timedelta(days=settings.jwt_refresh_token_expire_days))


def fingerprint_token(token: str) -> str:
    """Return a non-reversible representation safe to persist in the database."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode a token, raising JWTError when invalid or expired."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


__all__ = [
    "JWTError", "create_access_token", "create_refresh_token", "decode_access_token",
    "fingerprint_token", "hash_password", "verify_password",
]
