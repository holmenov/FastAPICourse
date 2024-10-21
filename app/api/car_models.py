from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException
from datetime import date

from app.api.dependencies import PaginationDep, DBDep
from app.exceptions import CarMarkNotFoundException, CarNotFoundByParametersException, CarNotFoundException
from app.schemas.car_models import (
    SCarModelsData,
    SCarModelsPatch,
    SCarModelsAddRequest,
    SCarModelsPatchRequest,
)
from app.schemas.features import SCarsFeaturesData


router = APIRouter(prefix="/cars", tags=["Автомобили"])


@router.get("/models/search", summary="Получить свободные автомобили для аренды")
@cache(expire=60)
async def get_cars_rent(
    pagination: PaginationDep,
    db: DBDep,
    mark_name: str | None = Query(None, description="Название модели", example="Toyota"),
    car_model_name: str | None = Query(None, description="Название модели", example="Land Cruiser"),
    car_model_year: int | None = Query(None, description="Год автомобиля", example="2015"),
    date_from: date = Query(None, description="Дата начала", example="2024-09-01"),
    date_to: date = Query(None, description="Дата окончания", example="2024-09-10"),
):
    per_page = pagination.per_page or 5
    try:
        data = await db.car_models.get_filtered_by_time(
            mark_name=mark_name,
            car_model_name=car_model_name,
            car_model_year=car_model_year,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )
    except CarNotFoundByParametersException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    return {"success": True, "data": data}


@router.get("/{mark_name}/models/{model_id}", summary="Получить автомобиль по ID")
@cache(expire=60)
async def get_car_model(db: DBDep, mark_name: str, model_id: int):
    car_data = await db.car_models.get_one_or_none(id=model_id, car_mark_name=mark_name)
    return {"success": True, "data": car_data}


@router.delete("/{mark_name}/models/{car_id}", summary="Удалить автомобиль")
async def delete_car(db: DBDep, mark_name: str, car_id: int):
    try:
        car_data = await db.car_models.get_car(id=car_id, car_mark_name=mark_name)
    except CarNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    
    await db.car_models.delete(id=car_id, car_mark_name=mark_name)
    await db.commit()
    return {"success": True}


@router.post("/{mark_name}/models", summary="Добавить автомобиль")
async def add_car_model(
    mark_name: str,
    db: DBDep,
    car_data: SCarModelsAddRequest = Body(),
):
    _car_data = SCarModelsData(car_mark_name=mark_name, **car_data.model_dump())
    try:
        added_car = await db.car_models.add_car_model(_car_data)
    except CarMarkNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    if car_data.features:
        features = [
            SCarsFeaturesData(car_id=added_car.id, feature_id=f_id) for f_id in car_data.features
        ]
        await db.cars_features.add_bulk(features)
    await db.commit()
    return {"success": True, "data": added_car}


@router.put("/{mark_name}/models/{car_id}", summary="Изменить данные об автомобиле полностью")
async def edit_car(mark_name: str, car_id: int, db: DBDep, car_data: SCarModelsAddRequest):
    _car_data = SCarModelsData(car_mark_name=mark_name, **car_data.model_dump())
    
    try:
        requsted_car = await db.car_models.get_car(id=car_id, car_mark_name=mark_name)
    except CarNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    
    await db.cars_features.update_features_bulk(car_id, car_data.features)
    await db.car_models.edit(_car_data, id=car_id, car_mark_name=mark_name)

    await db.commit()
    return {"success": True}


@router.patch("/{mark_name}/models/{car_id}", summary="Изменить данные об автомобиле частично")
async def partially_edit_car(
    mark_name: str, car_id: int, db: DBDep, car_data: SCarModelsPatchRequest
):
    _car_data_dict = car_data.model_dump(exclude_unset=True)
    _car_data = SCarModelsPatch(car_mark_name=mark_name, **_car_data_dict)
    
    try:
        requsted_car = await db.car_models.get_car(id=car_id, car_mark_name=mark_name)
    except CarNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    
    if "features" in _car_data_dict:
        await db.cars_features.update_features_bulk(car_id, car_data.features, exclude_unset=True)
    await db.car_models.edit(_car_data, id=car_id, car_mark_name=mark_name, exclude_unset=True)

    await db.commit()
    return {"success": True}
