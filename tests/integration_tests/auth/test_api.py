import pytest


@pytest.mark.parametrize("email, password, first_name, last_name, nickname", [
    ("user1@gmail.com", "123456", "Anton", "Ivanov", "ivanov_anton"),
    ("user2@gmail.com", "password123", "Andrey", "Petrov", "andrey1995"),
    ("user3@gmail.com", "useruserpass", "Nikolay", "Kozirev", "nikolakoz"),
])
async def test_auth(ac, email, password, first_name, last_name, nickname):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "nickname" : nickname
        }
    )
    assert response.status_code == 200
    
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert ac.cookies.get("access_token")
    
    response = await ac.get("/auth/me")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["data"]["email"] == email
    assert response_data["data"]["first_name"] == first_name
    assert response_data["data"]["last_name"] == last_name
    assert response_data["data"]["nickname"] == nickname
    
    response = await ac.post("/auth/logout")
    assert response.status_code == 200
    assert not ac.cookies.get("access_token")
    
    response = await ac.get("/auth/me")
    assert response.status_code == 401