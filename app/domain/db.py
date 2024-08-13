import sqlalchemy
from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = sqlalchemy.orm.declarative_base()


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    day = Column(Date)
    min_temp = Column(Float)
    max_temp = Column(Float)
    avg_temp = Column(Float)
    humidity = Column(Float)


class DB:
    def __enter__(self):
        url = "sqlite:///./weather.db"
        engine = create_engine(url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        self._db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()

    def add_weather_data(self, weather_data):
        (
            self._db.query(Weather)
            .filter(Weather.city == weather_data.city, Weather.day == weather_data.day)
            .delete()
        )
        self._db.add(weather_data)
        self._db.commit()

    def fetch_weather_data(self, city, day):
        return (
            self._db.query(Weather)
            .filter(Weather.city == city, Weather.day == day)
            .first()
        )
