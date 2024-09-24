from sqlalchemy import select, func, or_
from datetime import date

from app.database import engine
from app.models.bookings import BookingsORM
from app.models.car_models import CarModelsORM
from app.repositories.base import BaseRepository
from app.repositories.cars import CarsRepository
from app.schemas.car_models import SCarModels


class CarModelsRepository(BaseRepository):
    model = CarModelsORM
    schema = SCarModels


    async def get_filtred_by_time(
            self,
            mark_name: str | None,
            car_model_name: str | None,
            car_model_year: int | None,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int,
    ):
        all_booked_cars = (
            select(self.model, BookingsORM.date_from, BookingsORM.date_to)
            .outerjoin(BookingsORM, BookingsORM.car_id == self.model.id)
            .cte(name="all_booked_cars")
        )

        conditions = [
            or_(
                all_booked_cars.c.date_to <= date_from,
                all_booked_cars.c.date_from >= date_to,
                all_booked_cars.c.date_to.is_(None),
            )
        ]

        if mark_name:
            conditions.append(all_booked_cars.c.car_mark_name == mark_name)
        if car_model_name:
            conditions.append(all_booked_cars.c.car_model_name == car_model_name)
        if car_model_year:
            conditions.append(all_booked_cars.c.car_model_year == car_model_year)

        unbooked_cars_ids = (
            select(all_booked_cars.c.id)
            .distinct()
            .select_from(all_booked_cars)
            .filter(*conditions)
            .limit(limit).offset(offset)
        )

        return await self.get_all_filtered(self.model.id.in_(unbooked_cars_ids))