from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from app.database import async_session_maker, engine


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        data = await self.session.execute(query)
        return data.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        data = await self.session.execute(query)
        return data.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        data = await self.session.execute(add_data_stmt)
        return data.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        update_data_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by) -> None:
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)