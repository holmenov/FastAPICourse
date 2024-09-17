"""Init

Revision ID: 54318033f964
Revises: 
Create Date: 2024-09-17 11:32:31.915691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54318033f964'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mark', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('mark')
    )


def downgrade() -> None:
    op.drop_table('cars')
