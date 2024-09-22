from pydantic import BaseModel, ConfigDict


class SCarModelsData(BaseModel):
    car_mark_name: str
    car_model_name: str
    car_model_year: int
    description: str
    price: int

class SCarModelsAddRequest(BaseModel):
    car_mark_name: str
    car_model_year: int
    description: str
    price: int

class SCarModels(SCarModelsData):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SCarModelsPatch(BaseModel):
    car_mark_name: str | None = None
    car_model_name: str | None = None
    car_model_year: int | None = None
    description: str | None = None
    price: int | None = None

class SCarModelsPatchRequest(BaseModel):
    car_model_name: str | None = None
    car_model_year: int | None = None
    description: str | None = None
    price: int | None = None