from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("payload", postgresql.JSONB, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer, nullable=False, server_default="3"),
        sa.Column("last_error", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("started_at", sa.DateTime),
        sa.Column("finished_at", sa.DateTime),
    )


def downgrade():
    op.drop_table("jobs")
