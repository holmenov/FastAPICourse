from app.exceptions import check_date_to_after_date_from, ObjectNotFoundException, CarNotFoundException, \
    ObjectAlreadyExistException, CarAlreadyExistException
from app.schemas.car_models import SCarModelsAddRequest, SCarModelsData, SCarModelsPatchRequest
from app.schemas.features import SCarsFeaturesData
from app.service.base import BaseService


class CarModelsService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        mark_name,
        car_model_name,
        car_model_year,
        date_from,
        date_to
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        try:
            return await self.db.car_models.get_filtered_by_time(
                mark_name=mark_name,
                car_model_name=car_model_name,
                car_model_year=car_model_year,
                date_from=date_from,
                date_to=date_to,
                limit=per_page,
                offset=(pagination.page - 1) * per_page,
            )
        except ObjectNotFoundException as ex:
            raise CarNotFoundException from ex
    
    async def get_car_model(self, model_id: int, mark_name: str):
        return await self.get_model_with_check(id=model_id, car_mark_name=mark_name)
    
    async def delete_car(self, model_id: int, mark_name: str):
        await self.get_model_with_check(id=model_id, car_mark_name=mark_name)
        await self.db.car_models.delete(id=model_id, car_mark_name=mark_name)
        await self.db.commit()
    
    async def add_car(
        self,
        mark_name: str,
        car_data: SCarModelsAddRequest,
    ):
        _car_data = SCarModelsData(car_mark_name=mark_name, **car_data.model_dump())
        try:
            added_car = await self.db.car_models.add(_car_data)
        except ObjectAlreadyExistException as ex:
            raise CarAlreadyExistException from ex
        
        if car_data.features:
            features = [
                SCarsFeaturesData(car_id=added_car.id, feature_id=f_id) for f_id in car_data.features
            ]
            await self.db.cars_features.add_bulk(features)

        await self.db.commit()
        return added_car
    
    async def edit_car(self, mark_name: str, car_id: int, car_data: SCarModelsAddRequest):
        _car_data = SCarModelsData(car_mark_name=mark_name, **car_data.model_dump())
        
        await self.get_model_with_check(id=car_id, car_mark_name=mark_name)
        await self.db.cars_features.update_features_bulk(car_id, car_data.features)
        await self.db.car_models.edit(_car_data, id=car_id, car_mark_name=mark_name)
        await self.db.commit()
    
    async def partially_edit_car(self, mark_name: str, car_id: int, car_data: SCarModelsPatchRequest):
        _car_data_dict = car_data.model_dump(exclude_unset=True)
        _car_data = SCarModelsPatch(car_mark_name=mark_name, **_car_data_dict)
        await self.get_model_with_check(id=car_id, car_mark_name=mark_name)
        
        if "features" in _car_data_dict:
            await self.db.cars_features.update_features_bulk(car_id, car_data.features, exclude_unset=True)
        await self.db.car_models.edit(_car_data, id=car_id, car_mark_name=mark_name, exclude_unset=True)
        await self.db.commit()
    
    async def get_model_with_check(self, **filter_by):
        try:
            return await self.db.car_models.get_one(**filter_by)
        except ObjectNotFoundException as ex:
            raise CarNotFoundException from ex