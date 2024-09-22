from dns.reversename import from_address
from pydantic import BaseModel, Field, ConfigDict


class SCarsData(BaseModel):
    mark: str

class SCars(SCarsData):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SCarsPatch(BaseModel):
    mark: str | None = None