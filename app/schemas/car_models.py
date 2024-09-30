from pydantic import BaseModel

from app.schemas.features import SFeatures


class SCarModelsData(BaseModel):
    car_mark_name: str
    car_model_name: str
    car_model_year: int
    description: str
    price: int


class SCarModelsAddRequest(BaseModel):
    car_model_name: str
    car_model_year: int
    description: str
    price: int
    features: list[int] = []


class SCarModels(SCarModelsData):
    id: int


class ScarsWithRels(SCarModels):
    features: list[SFeatures]


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
    features: list[int] = []