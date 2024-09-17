from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description="Страница автомобилей")]
    per_page: Annotated[int, Query(5, ge=1, le=100, description="Автомобилей на каждой странице")]


PaginationDep = Annotated[PaginationParams, Depends()]