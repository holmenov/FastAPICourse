from pydantic import BaseModel, Field


class SCars(BaseModel):
    mark: str

class SCarsPATCH(BaseModel):
    mark: str | None = Field(None)