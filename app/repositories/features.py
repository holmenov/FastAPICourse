from app.models.features import FeaturesORM
from app.repositories.base import BaseRepository
from app.schemas.features import SFeatures


class FeaturesRepository(BaseRepository):
    model = FeaturesORM
    schema = SFeatures