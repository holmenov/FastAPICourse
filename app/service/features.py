from app.exceptions import ObjectAlreadyExistException, FeatureAlreadyExistException
from app.schemas.features import SFeaturesData
from app.service.base import BaseService


class FeaturesService(BaseService):
    async def get_all_features(self):
        return await self.db.features.get_all()
    
    async def create(self, data: SFeaturesData):
        try:
            feature = await self.db.features.add(data)
        except ObjectAlreadyExistException as ex:
            raise FeatureAlreadyExistException from ex
        await self.db.commit()
        return feature