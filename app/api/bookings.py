from fastapi import APIRouter, Body, Query, Depends
from fastapi.exceptions import HTTPException

from app.api.dependencies import PaginationDep, DBDep, UserIdDep
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