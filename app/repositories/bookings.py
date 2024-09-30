from app.models.bookings import BookingsORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper: DataMapper = BookingsDataMapper