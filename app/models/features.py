from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from app.database import Base


class FeaturesORM(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True)


class CarsFeaturesORM(Base):
    __tablename__ = "cars_features"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("car_models.id"))
    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))