from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.bookings import SBookingsAdd, SBookingsAddRequest


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование автомобилей"]
)


@router.post("", summary="Создание бронирование")
async def create_booking(db: DBDep, user_id: UserIdDep, data: SBookingsAddRequest = Body()):
    requested_car = await db.car_models.get_one_or_none(id=data.car_id)
    if requested_car is None:
        raise HTTPException(status_code=404, detail="Такого авто не существует")
    _data = SBookingsAdd(user_id=user_id, price=requested_car.price, **data.model_dump())
    booking = await db.bookings.add(_data)
    await db.commit()
    return {"success": True, "data": booking}


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"success": True, "data": bookings}


@router.get("/me", summary="Получить свои бронирования")
async def get_self_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_one_or_none(user_id=user_id)
    return {"success": True, "data": bookings}