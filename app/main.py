from datetime import date

from fastapi import FastAPI
from starlette import status
from starlette.responses import Response, JSONResponse

from app.domain.db import DB, Weather
from app.domain.errors import MissingCityData, OpenweatherAPIError
from app.domain.response_models import WeatherResponseModel
from app.service.open_weather import fetch_weather

app = FastAPI()


@app.post("/weather")
async def update_weather_data(city: str, day: date):
    """
    :param city: City to update weather data for.
    :param day: Date for data. Expected format "YYYY-MM-DD"
    """
    try:
        weather_data = fetch_weather(city, day)
    except MissingCityData:
        return JSONResponse(
            {"err": f"City '{city}' was not found in the openwweather database."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except OpenweatherAPIError as e:
        return JSONResponse(
            {"err": f"API error with Openweather. Error: {e}."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    with DB() as db:
        db.add_weather_data(
            Weather(
                city=city,
                day=day,
                humidity=weather_data.get("humidity"),
                min_temp=weather_data.get("min_temp"),
                max_temp=weather_data.get("max_temp"),
                avg_temp=weather_data.get("avg_temp"),
            )
        )
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/weather", response_model=WeatherResponseModel)
async def get_weather_data(city: str, day: date):
    """
    :param city: City to fetch weather data for.
    :param day: Date for data. Expected format "YYYY-MM-DD"
    """
    with DB() as db:
        city_data = db.fetch_weather_data(city, day)
    if not city_data:
        return JSONResponse(
            {"err": "City or date not found. Please update db using POST /weather."},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        {
            "max_temp": city_data.max_temp,
            "min_temp": city_data.min_temp,
            "avg_temp": city_data.avg_temp,
            "humidity": city_data.humidity,
        },
        status_code=status.HTTP_200_OK,
    )
