"""backfill_equipment_for_existing_workouts

Revision ID: a1b2c3d4e5f6
Revises: 659189cd7ffb
Create Date: 2025-12-31 18:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '659189cd7ffb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - backfill equipment from exercises table."""
    # Update workout_exercises by joining with exercises table to get equipment name
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            UPDATE workout_exercises we
            SET equipment = (
                SELECT eq.name
                FROM exercises e
                JOIN equipment eq ON e.equipment_id = eq.id
                WHERE e.id = we.exercise_id
            )
            WHERE we.equipment IS NULL
            AND we.exercise_id IS NOT NULL
        """)
    )


def downgrade() -> None:
    """Downgrade schema - clear backfilled equipment."""
    # This downgrade just clears the equipment field for records that were backfilled
    # We can't distinguish between manually entered and backfilled data,
    # so this is a best-effort downgrade
    pass
