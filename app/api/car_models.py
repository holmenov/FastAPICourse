from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.repositories.car_models import CarModelsRepository
from app.repositories.cars import CarsRepository
from app.schemas.car_models import SCarModelsData, SCarModelsPATCH
from app.schemas.cars import SCarsPATCH, SCarsData

router = APIRouter(
    prefix="/cars",
    tags=["Автомобили"]
)


@router.get("/{mark_name}/models", summary="Получить автомобили с заданными параметрами")
async def get_car_models(
        pagination: PaginationDep,
        mark_name: str,
        car_model_name: str | None = Query(None, description="Название модели"),
        car_model_year: int | None = Query(None, description="Год автомобиля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        data = await CarModelsRepository(session).get_all(
            car_mark_name=mark_name,
            car_model_name=car_model_name,
            car_model_year=car_model_year,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )
        return {"success": True, "data": data}

@router.get("/models/{model_id}", summary="Получить автомобиль по ID")
async def get_car_model(model_id: int):
    async with async_session_maker() as session:
        car_data = await CarModelsRepository(session).get_one_or_none(id=model_id)
    return {"success": True, "data": car_data}

@router.delete("/models/{car_id}", summary="Удалить автомобиль")
async def delete_car(car_id: int):
    async with async_session_maker() as session:
        car_data = await CarModelsRepository(session).get_one_or_none(id=car_id)
        if car_data:
            await CarModelsRepository(session).delete(id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}

@router.post("/models", summary="Добавить автомобиль")
async def add_car_model(car_data: SCarModelsData = Body()):
    async with async_session_maker() as session:
        added_car = await CarModelsRepository(session).add(car_data)
        await session.commit()
    return {"success": True, "data": added_car}

@router.put("/models/{car_id}", summary="Изменить данные об автомобиле полностью")
async def edit_car(car_id: int, car_data: SCarModelsData):
    async with async_session_maker() as session:
        requsted_car = await CarModelsRepository(session).get_one_or_none(id=car_id)
        if requsted_car:
            await CarModelsRepository(session).edit(car_data, id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}

@router.patch("/models/{car_id}", summary="Изменить данные об автомобиле частично")
async def partially_edit_car(car_id: int, car_data: SCarModelsPATCH):
    async with async_session_maker() as session:
        requsted_car = await CarModelsRepository(session).get_one_or_none(id=car_id)
        if requsted_car:
            await CarModelsRepository(session).edit(car_data, exclude_unset=True, id=car_id)
            await session.commit()
        else:
            raise HTTPException(status_code=404)
    return {"success": True}