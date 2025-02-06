from sqlmodel import SQLModel as BaseSQLModel, create_engine, Field
import os
from datetime import datetime

from ..config import settings
from ..schemas import *


from .database_init import create_test_data


class SQLModel(BaseSQLModel):
    # shared fields by all tables
    created_at: datetime = Field(default_factory=datetime.now(), nullable=False)
    created_by: int = Field(foreign_key='user.id')


engine = create_engine(settings.DATABASE_URL, echo=True)


if __name__ == "__main__":
    try:
        os.remove("./app/database/database.db")
    except FileNotFoundError:
        print("database file not exists")

    SQLModel.metadata.create_all(engine)

    create_test_data()
