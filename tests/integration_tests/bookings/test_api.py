import pytest

from app.database import async_session_maker_null_pool
from app.utils.db_manager import DBManager


@pytest.mark.parametrize("car_id, date_from, date_to, status_code",
    [
        (1, "2024-09-10", "2024-09-15", 200),
        (1, "2024-09-16", "2024-09-20", 200),
        (2, "2024-09-15", "2024-09-20", 200),
        (2, "2024-09-21", "2024-09-25", 200),
        (2, "2024-09-17", "2024-09-23", 409),
    ]
)
async def test_add_and_get_bookings(
        car_id, date_from, date_to, status_code, authenticated_ac, drop_all_bookings
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "car_id": car_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    
    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == 200
    assert response.json()["success"] == True


@pytest.fixture(scope="session")
async def drop_all_bookings():
    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.bookings.drop_all()
        await _db.commit()