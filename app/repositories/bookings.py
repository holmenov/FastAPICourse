from datetime import date

from sqlalchemy import select, or_, and_, not_

from app.models.bookings import BookingsORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper: DataMapper = BookingsDataMapper

    async def get_filtered_by_time(self, car_id: int, date_from: date, date_to: date):
        conditions = (
            and_(self.model.car_id == car_id),
            not_(
                or_(
                    self.model.date_to <= date_from,
                    self.model.date_from >= date_to,
                    self.model.date_to.is_(None),
                )
            ),
        )
        query = select(self.model).filter(*conditions)

        result = await self.session.execute(query)
        return [BookingsDataMapper.map_to_domain_entity(model) for model in result.scalars().all()]
