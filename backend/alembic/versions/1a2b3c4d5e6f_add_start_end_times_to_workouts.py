"""add_start_end_times_to_workouts

Revision ID: 1a2b3c4d5e6f
Revises: e0f1a2b3c4d5
Create Date: 2026-03-24 00:00:00.000000

"""
from datetime import timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, Sequence[str], None] = 'e0f1a2b3c4d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('workouts', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.add_column('workouts', sa.Column('end_time', sa.DateTime(), nullable=True))

    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id, date, duration FROM workouts")).fetchall()
    for row in rows:
        duration = row.duration or 0
        end_time = row.date
        start_time = end_time - timedelta(minutes=duration)
        conn.execute(
            sa.text(
                """
                UPDATE workouts
                SET start_time = :start_time,
                    end_time = :end_time
                WHERE id = :id
                """
            ),
            {
                "id": row.id,
                "start_time": start_time,
                "end_time": end_time,
            }
        )


def downgrade() -> None:
    op.drop_column('workouts', 'end_time')
    op.drop_column('workouts', 'start_time')
