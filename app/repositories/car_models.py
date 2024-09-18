from app.models.cars import CarsORM
from app.models.models import CarModelsORM
from app.repositories.base import BaseRepository


class CarModelsRepository(BaseRepository):
    model = CarModelsORM