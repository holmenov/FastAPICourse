from pydantic import BaseModel, EmailStr, Field


class SUserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str | None = Field(None)
    nickname: str


class SUserRequestLogin(BaseModel):
    email: EmailStr
    password: str


class SUserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str | None = Field(None)
    nickname: str


class SUsers(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str | None = Field(None)
    nickname: str


class SUserWithHashedPassword(SUsers):
    hashed_password: str