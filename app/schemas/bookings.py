from pydantic import BaseModel, ConfigDict
from datetime import date


class SBookingsAddRequest(BaseModel):
    date_from: date
    date_to: date
    car_id: int


class SBookingsAdd(SBookingsAddRequest):
    user_id: int
    price: int


class SBookings(SBookingsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)