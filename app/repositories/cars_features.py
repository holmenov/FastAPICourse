from app.models.features import CarsFeaturesORM
from app.repositories.base import BaseRepository
from app.schemas.car_features import SCarsFeatures


class CarsFeaturesRepository(BaseRepository):
    model = CarsFeaturesORM
    schema = SCarsFeatures