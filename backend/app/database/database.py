from sqlmodel import SQLModel, create_engine, Field, Column, DateTime, text
from pathlib import Path
from datetime import datetime, timezone
from contextlib import contextmanager
from sqlmodel import Session

from ..config import settings
from ..schemas import *


class UserAwareSession(Session):
    # database session with user context, to automatically set created_by and updated_by fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_user_id: int | None = None

    @contextmanager
    def user_context(self, user_id: int):
        old_user_id = self._current_user_id
        self._current_user_id = user_id
        try:
            yield
        finally:
            self._current_user_id = old_user_id

    def add(self, instance, *args, **kwargs):
        if hasattr(instance, "created_by") and instance.created_by is None:
            instance.created_by = self._current_user_id
        if hasattr(instance, "updated_by"):
            instance.updated_by = self._current_user_id
        return super().add(instance, *args, **kwargs)


def utcnow():
    return datetime.now(tz=timezone.utc)


class AutoFieldMixin:
    # shared fields by all tables
    created_at: datetime | None = Field(
        default_factory=utcnow, sa_type=DateTime(timezone=True))
    updated_at: datetime | None = Field(default_factory=utcnow, sa_type=DateTime(
        timezone=True), sa_column_kwargs={"onupdate": utcnow})

    created_by: int | None = Field(default=None, foreign_key='user.id')
    updated_by: int | None = Field(default=None, foreign_key='user.id')


# mysql+pymysql://user:password@localhost:3306/database
# sqlite:///database.db

if settings.ENV == "development":
    Path(__file__).parent.joinpath(
        f"{settings.DB_NAME}.db").unlink(missing_ok=True)
else:
    temp_engine = create_engine(
        f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}", echo=True)
    with temp_engine.connect() as conn:
        # clear the database if it exists
        conn.execute(text(f'DROP DATABASE IF EXISTS {settings.DB_NAME};'))
        # create the database
        conn.execute(
            text(f'CREATE DATABASE IF NOT EXISTS {settings.DB_NAME};'))
        conn.commit()

engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)

if __name__ == "__main__":

    SQLModel.metadata.create_all(engine)
    from .database_init import create_test_data
    create_test_data(engine)
