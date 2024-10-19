from pydantic import BaseModel


class SCarsData(BaseModel):
    mark: str


class SCars(SCarsData):
    id: int


class SCarsPatch(BaseModel):
    mark: str | None = None
