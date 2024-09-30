from app.models.bookings import BookingsORM
from app.models.car_models import CarModelsORM
from app.models.cars import CarsORM
from app.models.features import FeaturesORM, CarsFeaturesORM
from app.models.users import UsersORM
from app.repositories.mappers.base import DataMapper
from app.schemas.bookings import SBookings
from app.schemas.car_models import SCarModels, ScarsWithRels
from app.schemas.cars import SCars
from app.schemas.features import SFeatures, SCarsFeatures
from app.schemas.users import SUsers, SUserWithHashedPassword


class CarsDataMapper(DataMapper):
    db_model = CarsORM
    schema = SCars


class CarModelsDataMapper(DataMapper):
    db_model = CarModelsORM
    schema = SCarModels


class CarsWithRelsMapper(DataMapper):
    db_model = CarModelsORM
    schema = ScarsWithRels


class BookingsDataMapper(DataMapper):
    db_model = BookingsORM
    schema = SBookings


class FeaturesDataMapper(DataMapper):
    db_model = FeaturesORM
    schema = SFeatures


class CarFeaturesDataMapper(DataMapper):
    db_model = CarsFeaturesORM
    schema = SCarsFeatures


class UsersDataMapper(DataMapper):
    db_model = UsersORM
    schema = SUsers


class UsersHashedPasswordDataMapper(DataMapper):
    db_model = UsersORM
    schema = SUserWithHashedPassword