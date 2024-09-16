from fastapi import FastAPI, Body, Query
import uvicorn


app = FastAPI()

cars = [
    {"id": 1, "mark": "Toyota", "model": "Tundra"},
    {"id": 2, "mark": "Nissan", "model": "Qashqai"},
    {"id": 3, "mark": "Mazda", "model": "Mazda3"},
]

@app.get("/cars")
def get_cars(
        id: int | None = Query(None, description="ID Машины"),
        mark: str | None = Query(None, description="Название марки"),
        model: str | None = Query(None, description="Название модели"),
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
    return _cars

@app.delete("/cars/{car_id}")
def delete_car(
        car_id: int
):
    global cars
    cars = [car for car in cars if car["id"] != car_id]
    return {"success": True}

@app.post("/cars")
def add_car(
        id: int = Body(),
        mark: str = Body(),
        model: str = Body(),
):
    global cars
    cars.append({"id": id, "mark": mark, "model": model})
    return {"success": True}

@app.put("/cars/{car_id}")
def put_car(
        car_id: int,
        mark: str,
        model: str,
):
    global cars
    for car in cars:
        if car["id"] == car_id:
            car["mark"] = mark if mark else car["mark"]
            car["model"] = model if model else car["model"]
    return {"success": True}

@app.patch("/cars/{car_id}")
def patch_cars(
        car_id: int,
        mark: str | None = Query(None, description="Название марки"),
        model: str | None = Query(None, description="Название модели"),
):
    global cars
    for car in cars:
        if car["id"] == car_id:
            car["mark"] = mark if mark else car["mark"]
            car["model"] = model if model else car["model"]
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)