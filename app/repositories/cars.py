from sqlalchemy import select, func

from app.models.cars import CarsORM
from app.repositories.base import BaseRepository
from app.schemas.cars import SCars


class CarsRepository(BaseRepository):
    model = CarsORM
    schema = SCars

    async def get_all(self, mark, limit, offset) -> list[SCars]:
        query = select(CarsORM)
        if mark:
            query = query.filter(func.lower(CarsORM.mark) == mark.strip().lower())
        query = (query.limit(limit).offset(offset))
        data = await self.session.execute(query)
        return [
            SCars.model_validate(car, from_attributes=True) for car in data.scalars().all()
        ]