"""rename columns in car_models

Revision ID: 34751ae9586e
Revises: a646bce51a07
Create Date: 2024-09-21 18:25:26.474030

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "34751ae9586e"
down_revision: Union[str, None] = "a646bce51a07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "car_models", sa.Column("car_mark_name", sa.String(length=50), nullable=False)
    )
    op.add_column(
        "car_models", sa.Column("car_model_name", sa.String(length=50), nullable=False)
    )
    op.add_column(
        "car_models", sa.Column("car_model_year", sa.Integer(), nullable=False)
    )
    op.drop_constraint("car_models_mark_name_fkey", "car_models", type_="foreignkey")
    op.create_foreign_key(None, "car_models", "cars", ["car_mark_name"], ["mark"])
    op.drop_column("car_models", "mark_name")
    op.drop_column("car_models", "model_name")
    op.drop_column("car_models", "model_year")


def downgrade() -> None:
    op.add_column(
        "car_models",
        sa.Column("model_year", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "car_models",
        sa.Column(
            "model_name", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "car_models",
        sa.Column(
            "mark_name", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "car_models", type_="foreignkey")
    op.create_foreign_key(
        "car_models_mark_name_fkey", "car_models", "cars", ["mark_name"], ["mark"]
    )
    op.drop_column("car_models", "car_model_year")
    op.drop_column("car_models", "car_model_name")
    op.drop_column("car_models", "car_mark_name")
