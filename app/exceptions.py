class CarsRentException(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args):
        super().__init__(self.detail, *args)


class ObjectNotFoundException(CarsRentException):
    detail = "Объект не найден"


class UserAlreadyExistException(CarsRentException):
    detail = "Пользователь уже существует"


class IncorrectDataRentException(CarsRentException):
    detail = "Некорректные даты аренды автомобиля"


class CarNotFoundException(CarsRentException):
    detail = "Автомобиль не найден"


class CarNotFoundByParametersException(CarsRentException):
    detail = "Автомобиль по заданным параметрам не найден"


class CarMarkNotFoundException(CarsRentException):
    detail = "Марка автомобиля не найдена"