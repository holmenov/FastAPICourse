from app.models.users import UsersORM
from app.repositories.base import BaseRepository
from app.schemas.users import SUser


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = SUser