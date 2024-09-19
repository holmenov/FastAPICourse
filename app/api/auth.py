from fastapi import APIRouter
from passlib.context import CryptContext

from app.database import async_session_maker
from app.repositories.users import UsersRepository
from app.schemas.users import SUserRequestAdd, SUserAdd

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аунтефикация"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", summary="Регистрация пользователя")
async def register_user(data: SUserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    user_data = SUserAdd(
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
        nickname=str(data.nickname).lower(),
    )

    async with async_session_maker() as session:
        user = await UsersRepository(session).add(user_data)
        await session.commit()
    return {"success": True}