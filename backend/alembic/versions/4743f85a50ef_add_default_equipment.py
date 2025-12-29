"""add_default_equipment

Revision ID: 4743f85a50ef
Revises: 0258799edde7
Create Date: 2025-12-29 21:57:10.268362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '4743f85a50ef'
down_revision: Union[str, Sequence[str], None] = '0258799edde7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add default equipment
    default_equipment = [
        'Barbell',
        'Cable',
        'Dumbbell',
        'Kettlebell',
        'Bodyweight',
        'Treadmill',
        'Bike'
    ]

    conn = op.get_bind()
    for equipment_name in default_equipment:
        # Check if equipment already exists
        result = conn.execute(
            sa.text("SELECT id FROM equipment WHERE name = :name"),
            {"name": equipment_name}
        ).fetchone()

        if not result:
            # Insert if it doesn't exist
            conn.execute(
                sa.text("INSERT INTO equipment (id, name, archived) VALUES (:id, :name, :archived)"),
                {"id": str(uuid.uuid4()), "name": equipment_name, "archived": False}
            )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove default equipment
    default_equipment = [
        'Barbell',
        'Cable',
        'Dumbbell',
        'Kettlebell',
        'Bodyweight',
        'Treadmill',
        'Bike'
    ]

    conn = op.get_bind()
    for equipment_name in default_equipment:
        conn.execute(
            sa.text("DELETE FROM equipment WHERE name = :name"),
            {"name": equipment_name}
        )
