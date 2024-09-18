from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from app.database import Base


class CarModelsORM(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]