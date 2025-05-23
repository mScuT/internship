from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_min_price_filter() -> None:
    response = client.get("/items?min_price=4")
    assert all(item["price"] >= 4 for item in response.json())


def test_short_name() -> None:
    response = client.post("/items", json={"name": "ab", "price": 5})
    assert response.status_code == 422


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_item_name_consistency() -> None:
    item_name = "TestItem"
    item_price = 100.0
    client.post("/items", json={"name": item_name, "price": item_price})

    found = False
    skip = 0
    limit = 100

    while True:
        response = client.get(f"/items?min_price={item_price}&skip={skip}&limit={limit}")
        items = response.json()

        if not items:
            break

        if any(item["name"] == item_name for item in items):
            found = True
            break

        skip += limit
    assert found


def test_update_with_short_name() -> None:
    create_resp = client.post("/items", json={"name": "Apple", "price": 3.5})
    item_id = create_resp.json()["id"]
    update_resp = client.put(f"/items/{item_id}", json={"name": "ab"})
    assert update_resp.status_code == 422
    
    
def test_pagination() -> None:
    resp = client.get("/items?min_price=4&skip=50&limit=50")
    assert len(resp.json()) == 50
    assert all(item["price"] >= 4 for item in resp.json())
