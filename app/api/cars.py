from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select, func
from fastapi.exceptions import HTTPException

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.models.cars import CarsORM
from app.repositories.cars import CarsRepository
from app.schemas.cars import SCars, SCarsPATCH

router = APIRouter(
    prefix="/cars",
    tags=["Автомобили"]
)


@router.get("", summary="Получить автомобили с заданными параметрами")
async def get_cars(
        pagination: PaginationDep,
        id: int | None = Query(None, description="ID Автомобиля"),
        mark: str | None = Query(None, description="Название марки"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        data = await CarsRepository(session).get_all(
            id=id,
            mark=mark,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )
        return {"success": True, "data": data}

@router.delete("/{car_id}", summary="Удалить автомобиль")
async def delete_car(car_id: int):
    async with async_session_maker() as session:
        car_data = await CarsRepository(session).get_one_or_none(id=car_id)
        if car_data:
            await CarsRepository(session).delete(id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}

@router.post("", summary="Добавить автомобиль")
async def add_car(car_data: SCars = Body()):
    async with async_session_maker() as session:
        added_car = await CarsRepository(session).add(car_data)
        await session.commit()
    return {"success": True, "data": added_car}

@router.put("/{car_id}", summary="Изменить данные об автомобиле полностью")
async def put_car(car_id: int, car_data: SCars):
    async with async_session_maker() as session:
        car_data = await CarsRepository(session).get_one_or_none(id=car_id)
        if car_data:
            await CarsRepository(session).edit(car_data, id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}

@router.patch("/{car_id}", summary="Изменить данные об автомобиле частично")
def patch_car(car_id: int, car_data: SCarsPATCH):
    global cars
    car = [car for car in cars if car["id"] == car_id]

    if car_data.mark is not None:
        car["mark"] = car_data.mark
    if car_data.model is not None:
        car["model"] = car_data.model

    return {"success": True}