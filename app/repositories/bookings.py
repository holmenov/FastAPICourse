from sqlalchemy import select, func

from app.models.bookings import BookingsORM
from app.repositories.base import BaseRepository
from app.schemas.bookings import SBookings


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = SBookings