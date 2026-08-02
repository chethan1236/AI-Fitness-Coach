"""SQLAlchemy engine, declarative base, and unit-of-work session factory."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.debug,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(bind=engine, class_=Session, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class to inherit from for all ORM models."""


def get_db_session() -> Generator[Session, None, None]:
    """Yield one database session per request and always close it."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
