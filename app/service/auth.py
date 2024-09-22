from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone

from app.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = (
                datetime.now(timezone.utc)
                + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
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
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный формат токена авторизации")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Токен авторизации просрочен")
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Неверный токен авторизации")