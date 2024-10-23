from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query

from app.api.dependencies import PaginationDep, DBDep
from app.exceptions import CarNotFoundHTTPException, CarNotFoundException
from app.schemas.cars import SCarsPatch, SCarsData
from app.service.cars import CarsService


router = APIRouter(prefix="/cars", tags=["Марки автомобилей"])


@router.get("", summary="Получить марки автомобилей с заданными параметрами")
@cache(expire=60)
async def get_cars(
    pagination: PaginationDep,
    db: DBDep,
    mark: str | None = Query(None, description="Название марки"),
):
    data = await CarsService(db).get_all_cars(pagination=pagination, mark=mark)
    return {"success": True, "data": data}


@router.get("/{car_id}", summary="Получить марку автомобиля по ID")
@cache(expire=60)
async def get_car(car_id: int, db: DBDep):
    try:
        data = await CarsService(db).get_car_by_id(car_id=car_id)
    except CarNotFoundException:
        raise CarNotFoundHTTPException
    return {"success": True, "data": data}


@router.delete("/{mark_name}", summary="Удалить марку автомобиля")
async def delete_car(mark_name: str, db: DBDep):
    try:
        await CarsService(db).delete_car(mark_name=mark_name)
    except CarNotFoundException:
        raise CarNotFoundHTTPException
    return {"success": True}


@router.post("", summary="Добавить марку автомобиля")
async def add_car(db: DBDep, car_data: SCarsData = Body()):
    added_car = await CarsService(db).add_car(car_data=car_data)
    return {"success": True, "data": added_car}


@router.put("/{car_id}", summary="Изменить данные о марке автомобиля полностью")
async def edit_car(car_id: int, car_data: SCarsData, db: DBDep):
    try:
        await CarsService(db).edit_car(car_id=car_id, car_data=car_data)
    except CarNotFoundException:
        raise CarNotFoundHTTPException
    return {"success": True}


@router.patch("/{car_id}", summary="Изменить данные о марке автомобиля частично")
async def partially_edit_car(car_id: int, car_data: SCarsPatch, db: DBDep):
    try:
        await CarsService(db).partially_edit_car(car_id=car_id, car_data=car_data)
    except CarNotFoundException:
        raise CarNotFoundHTTPException
    return {"success": True}