from typing import Optional

from pydantic import BaseModel, Field


class WeatherResponseModel(BaseModel):
    min_temp: float = Field(
        ...,
        description="Minimum temperature recorded on day.",
    )
    max_temp: float = Field(
        ...,
        description="Maximum temperature recorded on day.",
    )
    avg_temp: float = Field(
        ...,
        description="Average temperature recorded on day.",
    )
    humidity: float = Field(
        ...,
        description="Humidity recorded on day.",
    )
