import pytest


class MockResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


@pytest.fixture()
def city_response_success():
    return MockResponse(
        [
            {
                "name": "London",
                "lat": 51.5073219,
                "lon": -0.1276474,
                "country": "GB",
                "state": "England",
            }
        ]
    )


@pytest.fixture()
def response_empty():
    return MockResponse([])


@pytest.fixture()
def response_failure():
    return MockResponse(
        {
            "cod": 401,
            "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.",
        }
    )


@pytest.fixture()
def weather_response():
    return MockResponse(
        {
            "lat": 51.5073219,
            "lon": -0.1276474,
            "tz": "+00:00",
            "date": "2023-01-01",
            "humidity": {"afternoon": 80.0},
            "temperature": {
                "min": 280.72,
                "max": 285.47,
                "afternoon": 284.8,
                "night": 285.47,
                "evening": 282.8,
                "morning": 283.89,
            },
        }
    )
