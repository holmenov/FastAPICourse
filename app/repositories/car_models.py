from sqlalchemy import select, func

from app.models.cars import CarsORM
from app.models.car_models import CarModelsORM
from app.repositories.base import BaseRepository
from app.schemas.car_models import SCarModels


class CarModelsRepository(BaseRepository):
    model = CarModelsORM
    schema = SCarModels

    async def get_all(
            self, car_mark_name, car_model_name, car_model_year, limit, offset
    ) -> list[SCarModels]:
        query = select(self.model)
        query = query.filter(func.lower(self.model.car_mark_name) == car_mark_name.strip().lower())
        if car_model_name:
            query = query.filter(func.lower(self.model.car_model_name) == car_model_name.strip().lower())
        if car_model_year:
            query = query.filter(func.lower(self.model.car_model_year) == car_model_year.strip().lower())
        query = (query.limit(limit).offset(offset))
        data = await self.session.execute(query)
        return [
            SCarModels.model_validate(car, from_attributes=True) for car in data.scalars().all()
        ]