from app.exceptions import ObjectNotFoundException, CarNotFoundException
from app.schemas.cars import SCarsData, SCarsPatch
from app.service.base import BaseService


class CarsService(BaseService):
    async def get_all_cars(self, pagination, mark: str):
        per_page = pagination.per_page or 5
        return await self.db.cars.get_all(
            mark=mark, limit=per_page, offset=(pagination.page - 1) * per_page
        )

    async def get_car_by_id(self, car_id: int):
        return await self.get_car_with_check(car_id=car_id)

    async def delete_car(self, car_id: str):
        await self.get_car_with_check(car_id=car_id)
        await self.db.cars.delete(car_id=car_id)
        await self.db.commit()

    async def add_car(self, car_data: SCarsData):
        added_car = await self.db.cars.add(car_data)
        await self.db.commit()
        return added_car

    async def edit_car(self, car_id: int, car_data: SCarsData):
        await self.get_car_with_check(car_id=car_id)
        await self.db.cars.edit(car_data, id=car_id)
        await self.db.commit()

    async def partially_edit_car(self, car_id: int, car_data: SCarsPatch):
        await self.get_car_with_check(car_id=car_id)
        await self.db.cars.edit(car_data, id=car_id, exclude_unset=True)
        await self.db.commit()

    async def get_car_with_check(self, **filter_by):
        try:
            await self.db.cars.get_one(**filter_by)
        except ObjectNotFoundException as ex:
            raise CarNotFoundException from ex
