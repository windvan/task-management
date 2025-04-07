from sqlmodel import Field, Enum as dbEnum, Relationship,DateTime,Column
from pydantic import EmailStr,field_validator
from datetime import datetime

from ..database.database import AutoFieldMixin, SQLModel
from .enums import DisciplineEnum
from ..utils.functions import date_to_utc


class CroBase(SQLModel):
    cro_name: str = Field(index=True, nullable=False, unique=True)
    certification_number: str = Field(unique=True)
    certification_scope: str
    certification_expiration_date: datetime
    address: str | None = None
    fw_contract_start: datetime | None = None
    fw_contract_end: datetime | None = None
    fw_contract_detail: str | None = None
    comments: str | None = None


class CroCreate(CroBase):
    pass


class CroPublic(CroBase):
    id: int


class CroUpdate(SQLModel):
    
    cro_name: str | None = None
    certification_number: str | None = None
    certification_scope: str | None = None
    certification_expiration_date: datetime | None = None
    address: str | None = None
    fw_contract_start: datetime | None = None
    fw_contract_end: datetime | None = None
    fw_contract_detail: str | None = None


class Cro(CroBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)

    contacts: list['CroContact'] = Relationship(back_populates='cro')
    tasks: list['Task'] = Relationship(back_populates='cro') # type: ignore

    # @field_validator('certification_expiration_date', 'fw_contract_start', 'fw_contract_end')
    # @classmethod
    # def date_field_validator(cls, v):
    #     return date_to_utc(v)

class CroContactBase(SQLModel):
    cro_id: int = Field(foreign_key="cro.id")
    contact_name: str = Field(unique=True)
    phone_number: str = Field(unique=True)
    email: EmailStr | None = None
    discipline: DisciplineEnum = Field(sa_column=dbEnum(DisciplineEnum))
    remarks: str | None = None



class CroContactCreate(CroContactBase):
    pass


class CroContactPublic(CroContactBase):
    id: int


class CroContactUpdate(SQLModel):
    created_by: int | None = None
    cro_id: int | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    discipline: DisciplineEnum | None = None
    comment: str | None = None


class CroContact(CroContactBase, AutoFieldMixin, table=True):
    __tablename__ = 'cro_contact'
    id: int | None = Field(default=None, primary_key=True)

    cro: Cro = Relationship(back_populates='contacts')

    