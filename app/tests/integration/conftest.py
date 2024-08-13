import datetime
import os

import pytest

from app.domain.db import Weather
from app.tests.integration.fake_local_db import TestDB


@pytest.fixture
def test_database():
    """Fixture to set up the sqlite database and teardown between each test"""
    if os.path.exists("test.db"):
        os.remove("test.db")

    with TestDB() as db:
        yield db

    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def basic_weather_data(test_database):
    weather = Weather(
        city="london",
        day=datetime.date(2023, 1, 1),
        min_temp=1,
        max_temp=3,
        avg_temp=2,
        humidity=5,
    )
    test_database.add(weather)
    test_database.commit()
