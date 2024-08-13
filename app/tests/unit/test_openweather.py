from unittest.mock import patch

import pytest

from app.domain.errors import MissingCityData, OpenweatherAPIError
from app.service.open_weather import fetch_city_data, fetch_weather


@patch("app.service.open_weather.requests.get")
def test_fetch_city_data_success(mock_request, city_response_success):
    mock_request.return_value = city_response_success
    assert fetch_city_data("a real city") == (51.5073219, -0.1276474)


@patch("app.service.open_weather.requests.get")
def test_fetch_city_data_no_data_for_city(mock_request, response_empty):
    mock_request.return_value = response_empty
    with pytest.raises(MissingCityData):
        fetch_city_data("a fake city")


@patch("app.service.open_weather.requests.get")
def test_fetch_city_data_api_error(mock_request, response_failure):
    mock_request.return_value = response_failure
    with pytest.raises(OpenweatherAPIError) as exec_data:
        fetch_city_data("a fake city")
        assert (
            str(exec_data.value)
            == "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
        )


@patch("app.service.open_weather.fetch_city_data")
@patch("app.service.open_weather.requests.get")
def test_fetch_weather_success(mock_request, mock_city_coords, weather_response):
    mock_city_coords.return_value = 1, 1
    mock_request.return_value = weather_response

    assert fetch_weather("a fake city", "2000-01-01") == {
        "humidity": 80.0,
        "max_temp": 285.47,
        "min_temp": 280.72,
        "avg_temp": 283.095,
    }


@patch("app.service.open_weather.fetch_city_data")
@patch("app.service.open_weather.requests.get")
def test_fetch_weather_api_error(mock_request, mock_city_coords, response_failure):
    mock_city_coords.return_value = 1, 1
    mock_request.return_value = response_failure

    with pytest.raises(OpenweatherAPIError) as exec_data:
        fetch_city_data("a fake city")
        assert (
            str(exec_data.value)
            == "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
        )
