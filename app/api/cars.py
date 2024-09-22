from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException

from app.api.dependencies import PaginationDep, DBDep
from app.schemas.cars import SCarsPatch, SCarsData

router = APIRouter(
    prefix="/cars",
    tags=["Марки автомобилей"]
)


@router.get("", summary="Получить марки автомобилей с заданными параметрами")
async def get_cars(
        pagination: PaginationDep,
        db: DBDep,
        mark: str | None = Query(None, description="Название марки"),
):
    per_page = pagination.per_page or 5
    data = await db.cars.get_all(
        mark=mark,
        limit=per_page,
        offset=(pagination.page - 1) * per_page
    )
    return {"success": True, "data": data}


@router.get("/{car_id}", summary="Получить марку автомобиля по ID")
async def get_car(car_id: int, db: DBDep):
    car_data = await db.cars.get_one_or_none(id=car_id)
    return {"success": True, "data": car_data}


@router.delete("/{mark_name}", summary="Удалить марку автомобиля")
async def delete_car(mark_name: str, db: DBDep):
    car_data = await db.cars.get_one_or_none(mark=mark_name)
    if car_data:
        await db.cars.delete(mark=mark_name)
    else:
        raise HTTPException(status_code=404)
    await db.commit()
    return {"success": True}


@router.post("", summary="Добавить марку автомобиля")
async def add_car(db: DBDep, car_data: SCarsData = Body()):
    added_car = await db.cars.add(car_data)
    await db.commit()
    return {"success": True, "data": added_car}


@router.put("/{car_id}", summary="Изменить данные о марке автомобиля полностью")
async def edit_car(car_id: int, car_data: SCarsData, db: DBDep):
    requested_car = await db.cars.get_one_or_none(id=car_id)
    if requested_car:
        await db.cars.edit(car_data, id=car_id)
    else:
        raise HTTPException(status_code=404)
    await db.commit()
    return {"success": True}


@router.patch("/{car_id}", summary="Изменить данные о марке автомобиля частично")
async def partially_edit_car(car_id: int, car_data: SCarsPatch, db: DBDep):
    requested_car = await db.cars.get_one_or_none(id=car_id)
    if requested_car:
        await db.cars.edit(car_data, id=car_id, exclude_unset=True)
    else:
        raise HTTPException(status_code=404)
    await db.commit()
    return {"success": True}