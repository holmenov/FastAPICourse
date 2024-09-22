from fastapi import APIRouter, HTTPException, Response, Request

from app.database import async_session_maker
from app.repositories.users import UsersRepository
from app.schemas.users import SUserRequestAdd, SUserAdd, SUserRequestLogin
from app.service.auth import AuthService
from app.api.dependencies import UserIdDep, DBDep


router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"]
)


@router.post("/register", summary="Регистрация пользователя")
async def register_user(data: SUserRequestAdd, db: DBDep):
    hashed_password = AuthService().get_password_hash(data.password)
    user_data = SUserAdd(
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
        nickname=str(data.nickname).lower(),
    )
    await db.users.add(user_data)
    await db.commit()
    return {"success": True}


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(db: DBDep, data: SUserRequestLogin, response: Response):
    user = await db.users.get_one_or_none(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователя не существует")
    user = await UsersRepository(db.session).get_user_with_hashed_password(user.email)
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль указан неверно")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"success": True, "access_token": access_token}


@router.post("/logout", summary="Выйти из аккаунта")
async def user_logout(response: Response):
    response.delete_cookie("access_token")
    return {"success": True}


@router.get("/me", summary="Получить информацию о себе")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return {"success": True, "data": user}