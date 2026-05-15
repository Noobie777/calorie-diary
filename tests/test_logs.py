from fastapi.testclient import TestClient
from main import app
from database import Base
from tests.test_database import engine,override_get_db
from routes.logs import get_db
import pytest
Base.metadata.create_all(engine)

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

client = TestClient(app)

def test_create_log():
    response = client.post("/logs", json={
        "food": "Test Food",
        "calories": 100,
        "protein": 10,
        "fiber": 2,
        "date": "2026-04-08"
    })
    assert response.status_code == 200
    data = response.json()

    assert data["food"] == "Test Food"
    assert data["calories"] == 100

def test_get_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_patch_log():
    create = client.post("/logs", json={
        "food": "Patch Food",
        "calories": 200,
        "protein": 15,
        "fiber": 3,
        "date": "2026-04-08"
    })
    log_id = create.json()["id"]

    response = client.patch(f"/logs/{log_id}", json={"calories": 300})

    assert response.status_code == 200
    data = response.json()
    assert data["calories"] == 300

def test_delete_log():
    create = client.post("/logs", json={
        "food": "Delete Food",
        "calories": 150,
        "protein": 12,
        "fiber": 2,
        "date": "2026-04-08"
    })
    log_id = create.json()["id"]
    response = client.delete(f"/logs/{log_id}")
    assert response.status_code == 200
    data = response.json()["message"] = "Log deleted"