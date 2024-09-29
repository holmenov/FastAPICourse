from sqlalchemy import select, func, or_
from datetime import date

from sqlalchemy.orm import joinedload, selectinload

from app.database import engine
from app.models.bookings import BookingsORM
from app.models.car_models import CarModelsORM
from app.repositories.base import BaseRepository
from app.repositories.cars import CarsRepository
from app.repositories.utils import get_unbooked_cars_ids
from app.schemas.car_models import SCarModels, ScarsWithRels


class CarModelsRepository(BaseRepository):
    model = CarModelsORM
    schema = SCarModels


    async def get_filtered_by_time(
            self,
            mark_name: str | None,
            car_model_name: str | None,
            car_model_year: int | None,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int,
    ):
        unbooked_cars_ids = get_unbooked_cars_ids(
            mark_name, car_model_name, car_model_year,
            date_from, date_to,
            limit, offset,
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.features))
            .filter(self.model.id.in_(unbooked_cars_ids))
        )
        result = await self.session.execute(query)
        return [
            ScarsWithRels.model_validate(
                model, from_attributes=True
            ) for model in result.scalars().all()
        ]