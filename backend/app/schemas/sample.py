from sqlmodel import Field, Enum as dbEnum, Relationship, Column, DateTime
from datetime import datetime
from pydantic import field_validator

from ..utils.functions import date_to_utc
from ..database.database import AutoFieldMixin, SQLModel
from .enums import SampleStatusEnum


class SampleBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    sample_name: str
    sample_status: SampleStatusEnum = Field(
        default=SampleStatusEnum.Waiting, sa_column=dbEnum(SampleStatusEnum))
    sample_quantity: str | None = None
    batch_number: str | None = None
    sealing_number: str | None = None
    production_date: datetime | None = None
    expiration_date: datetime | None = None
    shipped_quantity: int | None = None
    receiver_information: str | None = None


class SampleCreate(SampleBase):
    pass


class SamplePublic(SampleBase):
    id: int


class SampleUpdate(SQLModel):
    task_id: int | None = None
    sample_status: SampleStatusEnum | None = None
    sample_quantity: str | None = None
    batch_number: str | None = None
    sealing_number: str | None = None
    production_date: datetime | None = None
    expiration_date: datetime | None = None
    shipped_quantity: int | None = None
    receiver_information: str | None = None


class Sample(SampleBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)

    product: "Product" = Relationship(back_populates="samples")  # type: ignore
    tasks: list["Task"] = Relationship(back_populates="sample")  # type: ignore

    # @field_validator('production_date', 'expiration_date')
    # @classmethod
    # def date_field_validator(cls, v):
    #     return date_to_utc(v)
