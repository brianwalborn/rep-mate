"""add_cascade_to_template_fks

Revision ID: e0f1a2b3c4d5
Revises: d9e0f1a2b3c4
Create Date: 2026-02-27 03:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0f1a2b3c4d5'
down_revision: Union[str, Sequence[str], None] = 'd9e0f1a2b3c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing foreign key constraints and recreate with CASCADE
    
    # Drop and recreate template_sets foreign key with CASCADE
    op.drop_constraint('template_sets_template_exercise_id_fkey', 'template_sets', type_='foreignkey')
    op.create_foreign_key(
        'template_sets_template_exercise_id_fkey',
        'template_sets',
        'template_exercises',
        ['template_exercise_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # Drop and recreate template_exercises foreign keys with CASCADE
    op.drop_constraint('template_exercises_template_id_fkey', 'template_exercises', type_='foreignkey')
    op.create_foreign_key(
        'template_exercises_template_id_fkey',
        'template_exercises',
        'templates',
        ['template_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert to foreign keys without CASCADE
    op.drop_constraint('template_sets_template_exercise_id_fkey', 'template_sets', type_='foreignkey')
    op.create_foreign_key(
        'template_sets_template_exercise_id_fkey',
        'template_sets',
        'template_exercises',
        ['template_exercise_id'],
        ['id']
    )
    
    op.drop_constraint('template_exercises_template_id_fkey', 'template_exercises', type_='foreignkey')
    op.create_foreign_key(
        'template_exercises_template_id_fkey',
        'template_exercises',
        'templates',
        ['template_id'],
        ['id']
    )
