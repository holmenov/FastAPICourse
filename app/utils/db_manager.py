from app.repositories.car_models import CarModelsRepository
from app.repositories.cars import CarsRepository
from app.repositories.users import UsersRepository
from app.repositories.bookings import BookingsRepository
from app.repositories.features import FeaturesRepository, CarsFeaturesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.cars = CarsRepository(self.session)
        self.car_models = CarModelsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.features = FeaturesRepository(self.session)
        self.cars_features = CarsFeaturesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()