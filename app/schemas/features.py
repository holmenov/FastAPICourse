from pydantic import BaseModel


class SFeaturesData(BaseModel):
    title: str


class SFeatures(SFeaturesData):
    id: int


class SCarsFeaturesData(BaseModel):
    car_id: int
    feature_id: int


class SCarsFeatures(SCarsFeaturesData):
    id: int