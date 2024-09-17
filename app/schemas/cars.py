from pydantic import BaseModel, Field


class SCars(BaseModel):
    mark: str
    model: str

class SCarsPATCH(BaseModel):
    mark: str | None = Field(None)
    model: str | None = Field(None)