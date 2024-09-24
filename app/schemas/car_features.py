from pydantic import BaseModel, ConfigDict


class SCarsFeaturesData(BaseModel):
    car_id: int
    feature_id: int

class SCarsFeatures(SCarsFeaturesData):
    id: int

    model_config = ConfigDict(from_attributes=True)