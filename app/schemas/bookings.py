from pydantic import BaseModel
from datetime import date


class SBookingsAddRequest(BaseModel):
    car_id: int
    date_from: date
    date_to: date


class SBookingsAdd(SBookingsAddRequest):
    user_id: int
    price: int


class SBookings(SBookingsAdd):
    id: int
