"""add_equipment_to_workout_exercises

Revision ID: 659189cd7ffb
Revises: 4743f85a50ef
Create Date: 2025-12-31 18:03:56.145669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '659189cd7ffb'
down_revision: Union[str, Sequence[str], None] = '4743f85a50ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('workout_exercises', sa.Column('equipment', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('workout_exercises', 'equipment')
