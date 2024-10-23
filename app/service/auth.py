from fastapi import HTTPException, Response
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.exceptions import ObjectAlreadyExistException, UserAlreadyExistException, ObjectNotFoundException, \
    UserNotFoundException, PasswordNotMatchException
from app.repositories.users import UsersRepository
from app.schemas.users import SUserRequestAdd, SUserAdd, SUserRequestLogin
from app.service.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    async def register_user(self, data: SUserRequestAdd):
        hashed_password = self.get_password_hash(data.password)
        user_data = SUserAdd(
            email=data.email,
            hashed_password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            nickname=str(data.nickname).lower(),
        )
        try:
            await self.db.users.add(user_data)
        except ObjectAlreadyExistException as ex:
            raise UserAlreadyExistException from ex
        await self.db.commit()
        return user_data
    
    async def login_user(self, data: SUserRequestLogin, response: Response):
        try:
            user = await self.db.users.get_one(email=data.email)
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex
        
        user = await UsersRepository(self.db.session).get_user_with_hashed_password(user.email)
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise PasswordNotMatchException
        
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token
    
    async def get_me(self, user_id):
        try:
            return await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный формат токена авторизации")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Токен авторизации просрочен")
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Неверный токен авторизации")
