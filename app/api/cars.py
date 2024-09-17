from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.models.cars import CarsORM
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
        query = select(CarsORM)
        if id:
            query = query.filter_by(id=id)
        if mark:
            query = query.filter_by(mark=mark)
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        data = await session.execute(query)
        return data.scalars().all()

@router.delete("/{car_id}", summary="Удалить автомобиль")
def delete_car(
        car_id: int
):
    global cars
    cars = [car for car in cars if car["id"] != car_id]
    return {"success": True}

@router.post("", summary="Добавить автомобиль")
async def add_car(car_data: SCars = Body(openapi_examples={
    "1": {
        "summary": "Toyota",
        "value": {"mark": "Toyota"}
    },
    "2": {
        "summary": "Nissan",
        "value": {"mark": "Nissan"}
    },
})):
    async with async_session_maker() as session:
        add_car_stmt = insert(CarsORM).values(**car_data.model_dump())
        await session.execute(add_car_stmt)
        await session.commit()
    return {"success": True}

@router.put("/{car_id}", summary="Изменить данные об автомобиле полностью")
def put_car(
        car_id: int,
        mark: str = Body(description="Название марки"),
        model: str = Body(description="Название модели"),
):
    global cars
    car = [car for car in cars if car["id"] == car_id]
    car["mark"] = mark
    car["model"] = model
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