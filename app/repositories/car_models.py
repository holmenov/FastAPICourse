from sqlalchemy import select
from datetime import date

from sqlalchemy.orm import selectinload

from app.exceptions import ObjectNotFoundException
from app.models.car_models import CarModelsORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import CarModelsDataMapper, CarsWithRelsMapper
from app.repositories.utils import get_unbooked_cars_ids


class CarModelsRepository(BaseRepository):
    model = CarModelsORM
    mapper: DataMapper = CarModelsDataMapper

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).options(selectinload(self.model.features)).filter_by(**filter_by)
        data = await self.session.execute(query)
        model = data.scalars().one_or_none()
        if model is None:
            return None
        return CarsWithRelsMapper.map_to_domain_entity(model)

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
            mark_name,
            car_model_name,
            car_model_year,
            date_from,
            date_to,
            limit,
            offset,
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.features))
            .filter(self.model.id.in_(unbooked_cars_ids))
        )
        result = await self.session.execute(query)
        result_scalars = result.scalars().all()

        if not result_scalars:
            raise ObjectNotFoundException

        return [CarsWithRelsMapper.map_to_domain_entity(model) for model in result_scalars]
