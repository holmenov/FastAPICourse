from pydantic import BaseModel, ConfigDict


class SFeaturesData(BaseModel):
    title: str


class SFeatures(SFeaturesData):
    id: int

    model_config = ConfigDict(from_attributes=True)