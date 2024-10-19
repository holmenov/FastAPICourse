import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from app.database import Base

if typing.TYPE_CHECKING:
    from app.models import FeaturesORM


class CarModelsORM(Base):
    __tablename__ = "car_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_mark_name: Mapped[int] = mapped_column(ForeignKey("cars.mark"))
    car_model_name: Mapped[str] = mapped_column(String(50))
    car_model_year: Mapped[int]
    description: Mapped[str | None]
    price: Mapped[int]

    features: Mapped[list["FeaturesORM"]] = relationship(
        back_populates="car_models",
        secondary="cars_features"
    )