"""add profile fields to users table

Revision ID: 20260802_0002
Revises: 20260802_0001
Create Date: 2026-08-02
"""

from alembic import op
import sqlalchemy as sa

revision = "20260802_0002"
down_revision = "20260802_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("workout_days", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("preferred_workout_time", sa.String(length=32), nullable=True))
    op.add_column("users", sa.Column("diet_preference", sa.String(length=64), nullable=True))
    op.add_column("users", sa.Column("daily_calorie_goal", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "daily_calorie_goal")
    op.drop_column("users", "diet_preference")
    op.drop_column("users", "preferred_workout_time")
    op.drop_column("users", "workout_days")
