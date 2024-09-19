from pydantic import EmailStr
from sqlalchemy import select

from app.models.users import UsersORM
from app.repositories.base import BaseRepository
from app.schemas.users import SUser, SUserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = SUser

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        data = await self.session.execute(query)
        model = data.scalars().one()
        return SUserWithHashedPassword.model_validate(model, from_attributes=True)