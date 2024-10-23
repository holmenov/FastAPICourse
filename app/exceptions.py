from fastapi import HTTPException


class CarsRentException(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(CarsRentException):
    detail = "Объект не найден"


class ObjectAlreadyExistException(CarsRentException):
    detail = "Объект уже существует"


class CarNotFoundException(CarsRentException):
    detail = "Автомобиль не найден"


class CarAlreadyExistException(CarsRentException):
    detail = "Автомобиль уже существует"


class CarAlreadyBookedException(CarsRentException):
    detail = "Автомобиль уже забронирован"


class UserAlreadyExistException(CarsRentException):
    detail = "Пользователь с такой почтой уже существует"
    

class UserNotFoundException(CarsRentException):
    detail = "Пользователь не найден"


class PasswordNotMatchException(CarsRentException):
    detail = "Был введен неверный пароль"


class BookingsNotFoundException(CarsRentException):
    detail = "Бронирования не найдены"


class FeatureAlreadyExistException(CarsRentException):
    detail = "Такая особенность автомобиля уже существует"


def check_date_to_after_date_from(date_from, date_to):
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Некорректные даты аренды автомобиля")


class CarsRentHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CarNotFoundHTTPException(CarsRentHTTPException):
    status_code = 404
    detail = "Автомобиль не найден"


class CarAlreadyBookedHTTPException(CarsRentHTTPException):
    status_code = 409
    detail = "Автомобиль уже забронирован"


class CarAlreadyExistHTTPException(CarsRentHTTPException):
    status_code = 409
    detail = "Автомобиль уже существует"


class UserAlreadyExistHTTPException(CarsRentHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class UserNotFoundHTTPException(CarsRentHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class PasswordNotMatchHTTPException(CarsRentHTTPException):
    status_code = 401
    detail = "Был введен неверный пароль"


class BookingsNotFoundHTTPException(CarsRentHTTPException):
    status_code = 404
    detail = "Бронирования не найдены"


class FeatureAlreadyExistHTTPException(CarsRentHTTPException):
    status_code = 409
    detail = "Такая особенность автомобиля уже существует"


class IncorrectTokenHTTPException(CarsRentHTTPException):
    status_code = 401
    detail = "Некорректный токен"