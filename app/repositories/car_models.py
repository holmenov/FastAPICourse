from sqlalchemy import select, func, or_
from datetime import date

from app.database import engine
from app.models.bookings import BookingsORM
from app.models.car_models import CarModelsORM
from app.repositories.base import BaseRepository
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
            select(
                self.model.id,
                self.model.car_mark_name,
                self.model.car_model_name,
                self.model.car_model_year,
                self.model.price,
                self.model.description,
                BookingsORM.date_from,
                BookingsORM.date_to
            )
            .select_from(self.model)
            .outerjoin(BookingsORM, BookingsORM.car_id == self.model.id)
            .cte(name="all_booked_cars")
        )

        not_booked_cars = (
            select(
                all_booked_cars.c.id,
                all_booked_cars.c.car_mark_name,
                all_booked_cars.c.car_model_name,
                all_booked_cars.c.car_model_year,
                all_booked_cars.c.price,
                all_booked_cars.c.description,
            )
            .select_from(all_booked_cars)
            .filter(
                or_(
                    all_booked_cars.c.date_to <= date_from,
                    all_booked_cars.c.date_from >= date_to,
                    all_booked_cars.c.date_to.is_(None),
                )
            )
            .cte(name="not_booked_cars")
        )

        query = select(not_booked_cars).distinct().select_from(not_booked_cars)

        if mark_name:
            query = query.filter(not_booked_cars.c.car_mark_name == mark_name)
        if car_model_name:
            query = query.filter(not_booked_cars.c.car_model_name == car_model_name)
        if car_model_year:
            query = query.filter(not_booked_cars.c.car_model_year == car_model_year)

        query = (query.limit(limit).offset(offset))

        data = await self.session.execute(query)
        return [
            SCarModels.model_validate(car, from_attributes=True) for car in data.all()
        ]