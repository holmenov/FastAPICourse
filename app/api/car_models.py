from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query
from datetime import date

from app.api.dependencies import PaginationDep, DBDep
from app.exceptions import (
    CarNotFoundHTTPException,
    CarNotFoundException,
    CarAlreadyExistException,
    CarAlreadyExistHTTPException
)
from app.schemas.car_models import SCarModelsAddRequest, SCarModelsPatchRequest
from app.service.car_models import CarModelsService


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
    try:
        data = await CarModelsService(db).get_filtered_by_time(
            pagination,
            mark_name,
            car_model_name,
            car_model_year,
            date_from,
            date_to
        )
    except CarNotFoundException as ex:
        raise CarNotFoundHTTPException from ex
    return {"success": True, "data": data}


@router.get("/{mark_name}/models/{model_id}", summary="Получить автомобиль по ID")
@cache(expire=60)
async def get_car_model(db: DBDep, mark_name: str, model_id: int):
    try:
        car_data = await CarModelsService(db).get_car_model(model_id=model_id, mark_name=mark_name)
    except CarNotFoundException as ex:
        raise CarNotFoundHTTPException from ex
    return {"success": True, "data": car_data}


@router.delete("/{mark_name}/models/{car_id}", summary="Удалить автомобиль")
async def delete_car(db: DBDep, mark_name: str, car_id: int):
    try:
        await CarModelsService(db).delete_car(model_id=car_id, mark_name=mark_name)
    except CarNotFoundException as ex:
        raise CarNotFoundHTTPException from ex
    return {"success": True}


@router.post("/{mark_name}/models", summary="Добавить автомобиль")
async def add_car_model(
    mark_name: str,
    db: DBDep,
    car_data: SCarModelsAddRequest = Body(),
):
    try:
        added_car = await CarModelsService(db).add_car(mark_name=mark_name, car_data=car_data)
    except CarAlreadyExistException as ex:
        raise CarAlreadyExistHTTPException from ex
    return {"success": True, "data": added_car}


@router.put("/{mark_name}/models/{car_id}", summary="Изменить данные об автомобиле полностью")
async def edit_car(mark_name: str, car_id: int, db: DBDep, car_data: SCarModelsAddRequest):
    try:
        await CarModelsService(db).edit_car(mark_name=mark_name, car_id=car_id, car_data=car_data)
    except CarNotFoundException as ex:
        raise CarNotFoundHTTPException from ex
    return {"success": True}


@router.patch("/{mark_name}/models/{car_id}", summary="Изменить данные об автомобиле частично")
async def partially_edit_car(mark_name: str, car_id: int, db: DBDep, car_data: SCarModelsPatchRequest):
    try:
        await CarModelsService(db).partially_edit_car(mark_name=mark_name, car_id=car_id, car_data=car_data)
    except CarNotFoundException as ex:
        raise CarNotFoundHTTPException from ex
    return {"success": True}
