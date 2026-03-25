"""fix_workout_time_backfill

Revision ID: 2b3c4d5e6f7a
Revises: 1a2b3c4d5e6f
Create Date: 2026-03-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b3c4d5e6f7a'
down_revision: Union[str, Sequence[str], None] = '1a2b3c4d5e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Correct rows produced by the original backfill where:
    # - date represented workout end time,
    # - start_time was incorrectly set equal to date,
    # - end_time was incorrectly set to date + duration.
    op.execute(
        sa.text(
            """
            UPDATE workouts
            SET start_time = date - (COALESCE(duration, 0) * INTERVAL '1 minute'),
                end_time = date
            WHERE start_time = date
              AND end_time = date + (COALESCE(duration, 0) * INTERVAL '1 minute')
            """
        )
    )


def downgrade() -> None:
    # No-op: this is a data correction migration.
    pass
