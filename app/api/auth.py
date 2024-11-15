from fastapi import APIRouter, Response

from app.exceptions import (
    UserAlreadyExistException,
    UserAlreadyExistHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    PasswordNotMatchException,
    PasswordNotMatchHTTPException,
)
from app.schemas.users import SUserRequestAdd, SUserRequestLogin
from app.service.auth import AuthService
from app.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(data: SUserRequestAdd, db: DBDep):
    try:
        user_data = await AuthService(db).register_user(data=data)
    except UserAlreadyExistException:
        raise UserAlreadyExistHTTPException
    return {"success": True, "data": user_data}


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(db: DBDep, data: SUserRequestLogin, response: Response):
    try:
        access_token = await AuthService(db).login_user(data=data, response=response)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    except PasswordNotMatchException as ex:
        raise PasswordNotMatchHTTPException from ex
    return {"success": True, "access_token": access_token}


@router.post("/logout", summary="Выйти из аккаунта")
async def user_logout(response: Response):
    response.delete_cookie("access_token")
    return {"success": True}


@router.get("/me", summary="Получить информацию о себе")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        user = await AuthService(db).get_me(user_id=user_id)
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    return {"success": True, "data": user}
