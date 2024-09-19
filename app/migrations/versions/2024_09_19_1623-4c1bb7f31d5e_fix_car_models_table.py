"""fix car_models table

Revision ID: 4c1bb7f31d5e
Revises: fcc618556b3d
Create Date: 2024-09-19 16:23:39.178312

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c1bb7f31d5e"
down_revision: Union[str, None] = "fcc618556b3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "car_models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mark_name", sa.String(length=50), nullable=False),
        sa.Column("model_name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mark_name"],
            ["cars.mark"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("models")


def downgrade() -> None:
    op.create_table(
        "models",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("mark_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("price", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("quantity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["mark_id"], ["cars.id"], name="models_mark_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="models_pkey"),
    )
    op.drop_table("car_models")
