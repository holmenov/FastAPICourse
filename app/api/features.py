from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.features import SFeaturesData


router = APIRouter(
    prefix="/features",
    tags=["Особенности автомобилей"]
)


@router.get("", summary="Получить все особенности автомобилей")
# @cache(expire=60)
async def get_facilities(db: DBDep):
    features = await db.features.get_all()
    return {"success": True, "data": features}


@router.post("", summary="Добавить новую особенность автомобиля")
async def create_feature(db: DBDep, data: SFeaturesData = Body()):
    feature = await db.features.add(data)
    await db.commit()
    return {"success": True, "data": feature}