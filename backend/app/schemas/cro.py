from sqlmodel import Field, Enum as dbEnum, Relationship
from pydantic import EmailStr
from datetime import date

from ..database.database import SQLModel
from .enums import DisciplineEnum


class CroBase(SQLModel):
    cro_name: str = Field(index=True, nullable=False, unique=True)
    certification_number: str = Field(unique=True)
    certification_scope: str
    certification_expiration_date: date
    address: str | None = None
    fw_contract_start: date | None = None
    fw_contract_end: date | None = None
    fw_contract_detail: str | None = None
    comments: str | None = None


class CroCreate(CroBase):
    created_by: int | None = None


class CroPublic(CroBase):
    id: int


class CroUpdate(SQLModel):
    created_by: int | None = None
    cro_name: str | None = None
    certification_number: str | None = None
    certification_scope: str | None = None
    certification_expiration_date: date | None = None
    address: str | None = None
    fw_contract_start: date | None = None
    fw_contract_end: date | None = None
    fw_contract_detail: str | None = None


class Cro(CroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    contacts: list['CroContact'] = Relationship(back_populates='cro')


class CroContactBase(SQLModel):
    cro_id: int = Field(foreign_key="cro.id")
    contact_name: str = Field(unique=True)
    phone_number: str = Field(unique=True)
    email: EmailStr | None = None
    discipline: DisciplineEnum = Field(sa_column=dbEnum(DisciplineEnum))
    remarks: str | None = None


class CroContactCreate(CroContactBase):
    created_by: int | None = None


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


class CroContact(CroContactBase, table=True):
    __tablename__ = 'cro_contact'
    id: int | None = Field(default=None, primary_key=True)

    cro: Cro = Relationship(back_populates='contacts')
