"""add_equipment_table

Revision ID: b8c3e9f12345
Revises: 649d9aa5accd
Create Date: 2025-12-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8c3e9f12345'
down_revision: Union[str, Sequence[str], None] = '649d9aa5accd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create equipment table
    op.create_table(
        'equipment',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('archived', sa.Boolean(), nullable=True, server_default='false'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Seed equipment table with existing equipment values
    op.execute("""
        INSERT INTO equipment (id, name, archived)
        SELECT
            gen_random_uuid()::text,
            equipment,
            false
        FROM (
            SELECT DISTINCT equipment
            FROM exercises
            WHERE equipment IS NOT NULL
            ORDER BY equipment
        ) AS distinct_equipment
    """)

    # Add equipment_id column to exercises
    op.add_column('exercises', sa.Column('equipment_id', sa.String(), nullable=True))

    # Update exercises to reference equipment IDs
    op.execute("""
        UPDATE exercises e
        SET equipment_id = eq.id
        FROM equipment eq
        WHERE e.equipment = eq.name
    """)

    # Make equipment_id not nullable and add foreign key
    op.alter_column('exercises', 'equipment_id', nullable=False)
    op.create_foreign_key(
        'fk_exercises_equipment_id',
        'exercises', 'equipment',
        ['equipment_id'], ['id']
    )

    # Drop old equipment column
    op.drop_column('exercises', 'equipment')


def downgrade() -> None:
    # Add back equipment column
    op.add_column('exercises', sa.Column('equipment', sa.String(), nullable=True))

    # Populate equipment column from equipment table
    op.execute("""
        UPDATE exercises e
        SET equipment = eq.name
        FROM equipment eq
        WHERE e.equipment_id = eq.id
    """)

    # Make equipment not nullable
    op.alter_column('exercises', 'equipment', nullable=False)

    # Drop foreign key and equipment_id column
    op.drop_constraint('fk_exercises_equipment_id', 'exercises', type_='foreignkey')
    op.drop_column('exercises', 'equipment_id')

    # Drop equipment table
    op.drop_table('equipment')
