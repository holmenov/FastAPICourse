from sqlalchemy import select, or_
from datetime import date

from app.models.bookings import BookingsORM
from app.models.car_models import CarModelsORM


def get_unbooked_cars_ids(
        mark_name: str | None,
        car_model_name: str | None,
        car_model_year: int | None,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
):
    all_booked_cars = (
        select(CarModelsORM, BookingsORM.date_from, BookingsORM.date_to)
        .outerjoin(BookingsORM, BookingsORM.car_id == CarModelsORM.id)
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

    return unbooked_cars_ids