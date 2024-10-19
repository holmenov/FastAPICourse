from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
import typing

from app.database import Base

if typing.TYPE_CHECKING:
    from app.models import CarModelsORM


class FeaturesORM(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True)

    car_models: Mapped[list["CarModelsORM"]] = relationship(
        back_populates="features",
        secondary="cars_features"
    )


class CarsFeaturesORM(Base):
    __tablename__ = "cars_features"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car_models.id"))
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))