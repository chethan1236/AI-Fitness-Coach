"""create chat history table

Revision ID: 20260802_0006
Revises: 20260802_0005
Create Date: 2026-08-02
"""

from alembic import op
import sqlalchemy as sa

revision = "20260802_0006"
down_revision = "20260802_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_chat_history_user_id", "chat_history", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_chat_history_user_id", table_name="chat_history")
    op.drop_table("chat_history")
