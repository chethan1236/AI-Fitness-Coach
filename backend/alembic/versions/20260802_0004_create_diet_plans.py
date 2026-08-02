"""create diet plans table

Revision ID: 20260802_0004
Revises: 20260802_0003
Create Date: 2026-08-02
"""

from alembic import op
import sqlalchemy as sa

revision = "20260802_0004"
down_revision = "20260802_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "diet_plans",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("plan_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_diet_plans_user_id", "diet_plans", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_diet_plans_user_id", table_name="diet_plans")
    op.drop_table("diet_plans")
