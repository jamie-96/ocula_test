from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.fake_local_db import TestDB

client = TestClient(app)


@patch("app.main.DB", TestDB)
def test_get_weather_data(basic_weather_data):
    response = client.get("/weather?city=london&day=2023-01-01")
    assert response.json() == {
        "avg_temp": 2.0,
        "humidity": 5.0,
        "max_temp": 3.0,
        "min_temp": 1.0,
    }
    assert response.status_code == 200


@patch("app.main.DB", TestDB)
def test_get_weather_data_fails_with_missing_data():
    response = client.get("/weather?city=london&day=2023-01-01")
    assert response.json() == {
        "err": "City or date not found. Please update db using POST /weather."
    }
    assert response.status_code == 404


@patch("app.main.DB", TestDB)
def test_get_weather_data_fails_with_incorrect_inputs():
    response = client.get("/weather?city=london&day=not_a_date")
    assert response.status_code == 422
