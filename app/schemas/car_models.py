from pydantic import BaseModel, Field, ConfigDict


class SCarModelsData(BaseModel):
    car_mark_name: str
    car_model_name: str
    car_model_year: int
    description: str
    price: int

class SCarModels(SCarModelsData):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SCarModelsPATCH(BaseModel):
    car_mark_name: str | None = Field(None)
    car_model_name: str | None = Field(None)
    car_model_year: int | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)