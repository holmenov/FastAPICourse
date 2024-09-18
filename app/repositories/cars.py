from sqlalchemy import select, func

from app.models.cars import CarsORM
from app.repositories.base import BaseRepository


class CarsRepository(BaseRepository):
    model = CarsORM

    async def get_all(self, id, mark, limit, offset):
        query = select(CarsORM)
        if id:
            query = query.filter_by(id=id)
        if mark:
            query = query.filter(func.lower(CarsORM.mark) == mark.strip().lower())
        query = (query.limit(limit).offset(offset))
        data = await self.session.execute(query)
        return data.scalars().all()