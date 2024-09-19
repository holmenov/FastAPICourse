from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from app.database import Base


class CarModelsORM(Base):
    __tablename__ = "car_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark_name: Mapped[int] = mapped_column(ForeignKey("cars.mark"))
    model_name: Mapped[str] = mapped_column(String(50))
    model_year = Mapped[int]
    description: Mapped[str | None]
    price: Mapped[int]