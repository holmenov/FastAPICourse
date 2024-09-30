from pydantic import EmailStr
from sqlalchemy import select

from app.models.users import UsersORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.base import DataMapper
from app.repositories.mappers.mappers import UsersDataMapper, UsersHashedPasswordDataMapper


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper: DataMapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        data = await self.session.execute(query)
        model = data.scalars().one()
        return UsersHashedPasswordDataMapper.map_to_domain_entity(model)