from app.models.features import FeaturesORM, CarsFeaturesORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import FeaturesDataMapper, CarFeaturesDataMapper
from app.schemas.features import SCarsFeaturesData


class FeaturesRepository(BaseRepository):
    model = FeaturesORM
    mapper: DataMapper = FeaturesDataMapper


class CarsFeaturesRepository(BaseRepository):
    model = CarsFeaturesORM
    mapper: DataMapper = CarFeaturesDataMapper

    async def update_features_bulk(self, car_id: int, features_ids: list):
        current_features_row = await self.get_all_filtered(car_id=car_id)
        current_features_ids = [feature.feature_id for feature in current_features_row]

        features_to_remove = set(current_features_ids) - set(features_ids)
        features_to_add = set(features_ids) - set(current_features_ids)

        if features_to_remove:
            await self.delete(self.model.feature_id.in_(features_to_remove), car_id=car_id)

        if features_to_add:
            new_features_row = [
                SCarsFeaturesData(car_id=car_id, feature_id=f_id) for f_id in features_to_add
            ]
            await self.add_bulk(new_features_row)
