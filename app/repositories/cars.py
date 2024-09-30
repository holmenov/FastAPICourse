from sqlalchemy import select, func

from app.models.cars import CarsORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import CarsDataMapper
from app.schemas.cars import SCars


class CarsRepository(BaseRepository):
    model = CarsORM
    mapper: DataMapper = CarsDataMapper

    async def get_all(self, mark, limit, offset) -> list[SCars]:
        query = select(self.model)
        if mark:
            query = query.filter(func.lower(self.model.mark) == mark.strip().lower())
        query = (query.limit(limit).offset(offset))
        data = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(car) for car in data.scalars().all()]