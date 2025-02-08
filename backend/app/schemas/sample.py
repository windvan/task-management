from sqlmodel import Field, Enum as dbEnum, Relationship
from datetime import date


from ..database.database import SQLModel
from .enums import SampleStatusEnum, QuantityUnitEnum


class SampleTaskRelationship(SQLModel, table=True):
    __tablename__ = "sample_task_rel"
    sample_id: int = Field(foreign_key="sample.id", primary_key=True)
    task_id: int = Field(foreign_key="task.id", primary_key=True)


class SampleBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    sample_name: str
    sample_status: SampleStatusEnum = Field(
        default=SampleStatusEnum.Waiting, sa_column=dbEnum(SampleStatusEnum))
    estimated_quantity: int | None = None
    estimated_quantity_unit: QuantityUnitEnum | None = Field(
        default=None, sa_column=dbEnum(QuantityUnitEnum))
    received_quantity: int | None = None
    received_quantity_unit: QuantityUnitEnum | None = Field(
        default=None, sa_column=dbEnum(QuantityUnitEnum))
    batch_number: str | None = None
    sealing_number: str | None = None
    production_date: date | None = None
    expiration_date: date | None = None
    shipped_quantity: int | None = None
    receiver_information: str | None = None


class SampleCreate(SampleBase):
    pass


class SamplePublic(SampleBase):
    id: int


class SampleUpdate(SQLModel):
    task_id: int | None = None
    sample_status: SampleStatusEnum | None = None
    estimated_quantity: int | None = None
    estimated_quantity_unit: QuantityUnitEnum | None = None
    received_quantity: int | None = None
    received_quantity_unit: QuantityUnitEnum | None = None
    batch_number: str | None = None
    sealing_number: str | None = None
    production_date: date | None = None
    expiration_date: date | None = None
    shipped_quantity: int | None = None
    receiver_information: str | None = None


class Sample(SampleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    tasks: list["Task"] = Relationship( # type: ignore
        back_populates="samples", link_model=SampleTaskRelationship)
