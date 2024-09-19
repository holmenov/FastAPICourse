from pydantic import BaseModel, ConfigDict, EmailStr, Field


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

class SUser(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str | None = Field(None)
    nickname: str

    model_config = ConfigDict(from_attributes=True)

class SUserWithHashedPassword(SUser):
    hashed_password: str