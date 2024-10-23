from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.exceptions import FeatureAlreadyExistException, FeatureAlreadyExistHTTPException
from app.schemas.features import SFeaturesData
from app.service.features import FeaturesService

router = APIRouter(prefix="/features", tags=["Особенности автомобилей"])


@router.get("", summary="Получить все особенности автомобилей")
@cache(expire=60)
async def get_facilities(db: DBDep):
    features = await FeaturesService(db).get_all_features()
    return {"success": True, "data": features}


@router.post("", summary="Добавить новую особенность автомобиля")
async def create_feature(db: DBDep, data: SFeaturesData = Body()):
    try:
        feature = await FeaturesService(db).create(data)
    except FeatureAlreadyExistException as ex:
        raise FeatureAlreadyExistHTTPException from ex
    return {"success": True, "data": feature}
