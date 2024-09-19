from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.repositories.cars import CarsRepository
from app.schemas.cars import SCarsPATCH, SCarsData

router = APIRouter(
    prefix="/cars",
    tags=["Автомобили"]
)


@router.get("", summary="Получить автомобили с заданными параметрами")
async def get_cars(
        pagination: PaginationDep,
        mark: str | None = Query(None, description="Название марки"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        data = await CarsRepository(session).get_all(
            mark=mark,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )
        return {"success": True, "data": data}

@router.get("/{car_id}", summary="Получить автомобиль по ID")
async def get_car(car_id: int):
    async with async_session_maker() as session:
        car_data = await CarsRepository(session).get_one_or_none(id=car_id)
    return {"success": True, "data": car_data}

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
async def add_car(car_data: SCarsData = Body()):
    async with async_session_maker() as session:
        added_car = await CarsRepository(session).add(car_data)
        await session.commit()
    return {"success": True, "data": added_car}

@router.put("/{car_id}", summary="Изменить данные об автомобиле полностью")
async def edit_car(car_id: int, car_data: SCarsData):
    async with async_session_maker() as session:
        car_data = await CarsRepository(session).get_one_or_none(id=car_id)
        if car_data:
            await CarsRepository(session).edit(car_data, id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}

@router.patch("/{car_id}", summary="Изменить данные об автомобиле частично")
async def partially_edit_car(car_id: int, car_data: SCarsPATCH):
    async with async_session_maker() as session:
        car_data = await CarsRepository(session).get_one_or_none(id=car_id)
        if car_data:
            await CarsRepository(session).edit(car_data, exclude_unset=True, id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}