from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base


class CarsORM(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[str] = mapped_column(String(50), unique=True)
