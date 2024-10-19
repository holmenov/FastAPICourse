async def test_add_features(ac):
    response = await ac.post("/features", json={"title": "Apple CarPlay"})
    assert response.status_code == 200


async def test_get_features(ac):
    response = await ac.get("/features")
    assert response.status_code == 200
