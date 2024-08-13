import requests

from app.config import API_KEY
from app.domain.errors import MissingCityData, OpenweatherAPIError


def fetch_city_data(city):
    """
    Using this to convert a city name to lat/long, since the API to fetch by city name has been deprecated
    """
    city_code_response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    )
    response_json = city_code_response.json()
    if not response_json:
        raise MissingCityData
    if isinstance(response_json, dict):
        raise OpenweatherAPIError(response_json.get("message"))
    return response_json[0].get("lat"), response_json[0].get("lon")


def fetch_weather(city, day):
    """
    Not explicitly catching errors for incorrect latitude and longitude in the request, as I'm assuming those will have
    been caught in the above func
    """
    lat, long = fetch_city_data(city)
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={day}&appid={API_KEY}"
    )
    response_json = weather_response.json()
    if response_json.get("message"):
        raise OpenweatherAPIError(response_json.get("message"))

    max_temp = response_json.get("temperature", {}).get("max")
    min_temp = response_json.get("temperature", {}).get("min")
    if min_temp and max_temp:
        avg_temp = (max_temp + min_temp) / 2
    else:
        avg_temp = None
    return {
        "humidity": response_json.get("humidity", {}).get("afternoon"),
        "max_temp": max_temp,
        "min_temp": min_temp,
        "avg_temp": avg_temp,
    }


if __name__ == "__main__":
    fetch_weather("london", "2023-01-01")
