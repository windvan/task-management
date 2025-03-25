from sqlmodel import SQLModel, create_engine, Field, Column, DateTime
from pathlib import Path
from datetime import datetime, timezone


from ..config import settings
from ..schemas import *


class AutoFieldMixin:
    # shared fields by all tables
    created_at: datetime | None = Field(default=None,sa)
    updated_at: datetime | None = Field(default=None, sa_column_kwargs={'onupdate': datetime.now(tz=timezone.utc)}),

    created_by: int | None = Field(default=None, foreign_key='user.id')
    updated_by: int | None = Field(default=None, foreign_key='user.id')


engine = create_engine(settings.DATABASE_URL, echo=True)

if __name__ == "__main__":

    Path(__file__).parent.joinpath("database.db").unlink(missing_ok=True)
    SQLModel.metadata.create_all(engine)
    from .database_init import create_test_data
    create_test_data(engine)
