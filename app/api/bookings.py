from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import CarAlreadyBookedHTTPException, \
    BookingsNotFoundException, BookingsNotFoundHTTPException, CarNotFoundException, CarNotFoundHTTPException, \
    CarAlreadyBookedException
from app.schemas.bookings import SBookingsAddRequest
from app.service.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирование автомобилей"])


@router.get("/all", summary="Получить все бронирования")
@cache(expire=10)
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"success": True, "data": bookings}


@router.get("/me", summary="Получить свои бронирования")
@cache(expire=10)
async def get_self_bookings(db: DBDep, user_id: UserIdDep):
    try:
        bookings = await BookingsService(db).get_self_bookings(user_id=user_id)
    except BookingsNotFoundException as ex:
        raise BookingsNotFoundHTTPException from ex
    return {"success": True, "data": bookings}


@router.post("", summary="Создание бронирование")
async def create_booking(db: DBDep, user_id: UserIdDep, data: SBookingsAddRequest = Body()):
    try:
        booking = await BookingsService(db).create_booking(user_id=user_id, data=data)
    except CarNotFoundException as ex:
        raise CarNotFoundHTTPException from ex
    except CarAlreadyBookedException as ex:
        raise CarAlreadyBookedHTTPException from ex
    return {"success": True, "data": booking}
