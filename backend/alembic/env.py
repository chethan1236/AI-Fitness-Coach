"""Alembic migration environment for the AI Fitness Coach database."""

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.database.database import Base
from app.models.user import RefreshToken, User  # noqa: F401

# Import ORM models here as they are introduced, so Alembic can discover them.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = context.config.get_section(context.config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.database_url
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
