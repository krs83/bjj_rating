"""add enum disciplines - gi or no-gi

Revision ID: 7107c757da66
Revises: ee442e2b725e
Create Date: 2026-06-10 20:09:18.952429

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa

from backend.src.models.athlete import Discipline

# revision identifiers, used by Alembic.
revision: str = '7107c757da66'
down_revision: Union[str, Sequence[str], None] = 'ee442e2b725e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('athlete', sa.Column('discipline',
                                       sqlmodel.sql.sqltypes.AutoString(),
                                       server_default=Discipline.GI.value,
                                       nullable=False))
    op.create_index(op.f('ix_athlete_discipline'), 'athlete', ['discipline'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_athlete_discipline'), table_name='athlete')
    op.drop_column('athlete', 'discipline')
