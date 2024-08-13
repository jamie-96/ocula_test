from unittest.mock import patch

from fastapi.testclient import TestClient

from app.domain.errors import MissingCityData, OpenweatherAPIError
from app.main import app
from app.tests.integration.fake_local_db import TestDB

client = TestClient(app)


@patch("app.main.DB", TestDB)
@patch("app.main.fetch_weather")
def test_post_weather_data(mock_openweather_data):
    mock_openweather_data.return_value = {
        "humidity": 1,
        "max_temp": 1,
        "min_temp": 1,
        "avg_temp": 1,
    }
    response = client.post("/weather?city=london&day=2023-01-01")
    assert response.status_code == 201


@patch("app.main.DB", TestDB)
@patch("app.main.fetch_weather")
def test_post_weather_data_updates_if_same_day_and_month(
    mock_openweather_data, basic_weather_data
):
    # Check existing db data for london on 01/01/2023
    response = client.get("/weather?city=london&day=2023-01-01")
    assert response.json() == {
        "avg_temp": 2.0,
        "humidity": 5.0,
        "max_temp": 3.0,
        "min_temp": 1.0,
    }

    # do another post request to update it
    mock_openweather_data.return_value = {
        "humidity": 1,
        "max_temp": 1,
        "min_temp": 1,
        "avg_temp": 1,
    }
    response = client.post("/weather?city=london&day=2023-01-01")
    assert response.status_code == 201

    # Check again for db data for london on 01/01/2023
    response = client.get("/weather?city=london&day=2023-01-01")
    assert response.json() == {
        "avg_temp": 1.0,
        "humidity": 1.0,
        "max_temp": 1.0,
        "min_temp": 1.0,
    }


@patch("app.main.DB", TestDB)
@patch("app.main.fetch_weather")
def test_post_weather_data_fails_if_missing_city(mock_openweather_data):
    mock_openweather_data.side_effect = MissingCityData
    response = client.post("/weather?city=london&day=2023-01-01")
    assert response.status_code == 400
    assert response.json() == {
        "err": f"City 'london' was not found in the openwweather database."
    }


@patch("app.main.DB", TestDB)
@patch("app.main.fetch_weather")
def test_post_weather_data_fails_if_openweather_api_issue(mock_openweather_data):
    mock_openweather_data.side_effect = OpenweatherAPIError("some error")
    response = client.post("/weather?city=london&day=2023-01-01")
    assert response.status_code == 400
    assert response.json() == {"err": f"API error with Openweather. Error: some error."}
