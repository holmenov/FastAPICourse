from fastapi import HTTPException


class CarsRentException(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(CarsRentException):
    detail = "Объект не найден"


class ObjectAlreadyExistException(CarsRentException):
    detail = "Объект уже существует"


def check_date_to_after_date_from(date_from, date_to):
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Некорректные даты аренды автомобиля")


class CarsRentHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CarNotFoundException(CarsRentHTTPException):
    status_code = 404
    detail = "Автомобиль не найден"


class CarAlreadyBookedException(CarsRentHTTPException):
    status_code = 409
    detail = "Автомобиль уже забронирован"