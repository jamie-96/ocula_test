from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.db import DB, Base


class TestDB(DB):
    def __enter__(self):
        # Database setup
        url = "sqlite:///./test.db"
        engine = create_engine(url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)

        self._db = SessionLocal()
        return self

    def add(self, obj):
        self._db.add(obj)

    def commit(self):
        self._db.commit()
