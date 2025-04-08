from sqlmodel import SQLModel  # base model for all tables
from sqlmodel import create_engine, Session, Field, DateTime
from datetime import datetime, timezone
from ..config import settings


class UserAwareSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_user_id: int | None = None

    def set_user_id(self, user_id: int):
        self._current_user_id = user_id
        return self

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


engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)


