from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from app.service.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description="Страница автомобилей")]
    per_page: Annotated[int | None, Query(None, ge=1, le=100, description="Автомобилей на каждой странице")]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Вы не аутентифицированы.")
    return access_token

def get_current_user_id(access_token: str = Depends(get_token)) -> int:
    token_data = AuthService().decode_token(access_token)
    return token_data.get("user_id")

UserIdDep = Annotated[PaginationParams, Depends(get_current_user_id)]