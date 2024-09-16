from fastapi import APIRouter, Body, Query

from schemas.cars import SCars, SCarsPATCH


router = APIRouter(
    prefix="/cars",
    tags=["Автомобили"]
)

cars = [
    {"id": 1, "mark": "Toyota", "model": "Tundra"},
    {"id": 2, "mark": "Nissan", "model": "Qashqai"},
    {"id": 3, "mark": "Mazda", "model": "Mazda3"},
    {"id": 4, "mark": "Honda", "model": "Civic"},
    {"id": 5, "mark": "Ford", "model": "Focus"},
    {"id": 6, "mark": "BMW", "model": "X5"},
    {"id": 7, "mark": "Audi", "model": "A4"},
    {"id": 8, "mark": "Mercedes-Benz", "model": "C-Class"},
    {"id": 9, "mark": "Subaru", "model": "Outback"}
]

@router.get("", summary="Получить автомобили с заданными параметрами")
def get_cars(
        id: int | None = Query(None, description="ID Автомобиля"),
        mark: str | None = Query(None, description="Название марки"),
        model: str | None = Query(None, description="Название модели"),
        page: int = Query(1, description="Страница автомобилей"),
        per_page: int = Query(5, description="Автомобилей на каждой странице"),
):
    _cars = []
    for car in cars:
        if id and car["id"] != id:
            continue
        if mark and car["mark"] != mark:
            continue
        if model and car["model"] != model:
            continue
        _cars.append(car)

    start_item = (page - 1) * per_page
    end_item = page * per_page

    return _cars[start_item:end_item]

@router.delete("/{car_id}", summary="Удалить автомобиль")
def delete_car(
        car_id: int
):
    global cars
    cars = [car for car in cars if car["id"] != car_id]
    return {"success": True}

@router.post("", summary="Добавить автомобиль")
def add_car(car_data: SCars):
    global cars
    cars.append({"id": cars[-1]["id"]+1, "mark": car_data.mark, "model": car_data.model})
    return {"success": True}

@router.put("/{car_id}", summary="Изменить данные об автомобиле полностью")
def put_car(
        car_id: int,
        mark: str = Body(description="Название марки"),
        model: str = Body(description="Название модели"),
):
    global cars
    car = [car for car in cars if car["id"] == car_id]
    car["mark"] = mark
    car["model"] = model
    return {"success": True}

@router.patch("/{car_id}", summary="Изменить данные об автомобиле частично")
def patch_car(car_id: int, car_data: SCarsPATCH):
    global cars
    car = [car for car in cars if car["id"] == car_id]

    if car_data.mark is not None:
        car["mark"] = car_data.mark
    if car_data.model is not None:
        car["model"] = car_data.model

    return {"success": True}