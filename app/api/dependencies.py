from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from app.database import async_session_maker
from app.exceptions import IncorrectTokenHTTPException
from app.service.auth import AuthService
from app.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description="Страница автомобилей")]
    per_page: Annotated[
        int | None, Query(None, ge=1, le=100, description="Автомобилей на каждой странице")
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise IncorrectTokenHTTPException
    return access_token


def get_current_user_id(access_token: str = Depends(get_token)) -> int:
    token_data = AuthService().decode_token(access_token)
    return token_data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db() -> DBManager:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
