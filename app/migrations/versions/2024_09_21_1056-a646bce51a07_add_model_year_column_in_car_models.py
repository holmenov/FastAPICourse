"""add model_year column in car_models

Revision ID: a646bce51a07
Revises: 4c1bb7f31d5e
Create Date: 2024-09-21 10:56:08.068193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a646bce51a07"
down_revision: Union[str, None] = "4c1bb7f31d5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("car_models", sa.Column("model_year", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("car_models", "model_year")
