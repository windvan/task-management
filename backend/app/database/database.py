from sqlmodel import SQLModel as BaseSQLModel, create_engine, Field, Session
from pathlib import Path
from datetime import datetime


from ..config import settings
from ..schemas import *


class SQLModel(BaseSQLModel):
    # shared fields by all tables
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: int | None = Field(default=None,foreign_key='user.id')


engine = create_engine(settings.DATABASE_URL, echo=True)

if __name__ == "__main__":

    Path(__file__).parent.joinpath("database.db").unlink(missing_ok=True)
    SQLModel.metadata.create_all(engine)
    from .database_init import create_test_data
    create_test_data(engine)
