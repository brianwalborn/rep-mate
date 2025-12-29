"""add_notes_to_workout_exercises

Revision ID: 0258799edde7
Revises: b8c3e9f12345
Create Date: 2025-12-29 21:39:06.604529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0258799edde7'
down_revision: Union[str, Sequence[str], None] = 'b8c3e9f12345'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('workout_exercises', sa.Column('notes', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('workout_exercises', 'notes')
