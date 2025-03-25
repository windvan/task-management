from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel, Enum as dbEnum, Relationship

from ..database.database import AutoFieldMixin, SQLModel  # 保持这种导入方法以确保数据库表的一致性
from ..schemas.enums import RoleEnum
from ..schemas.message import MessageRecipient


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    name: str = Field(unique=True)
    role: RoleEnum = Field(sa_column=dbEnum(RoleEnum))

    @field_validator('email')
    @classmethod
    def format_email(cls, v: str):
        return v.lower()

    @field_validator('name')
    @classmethod
    def format_name(cls, v: str):
        return v.title()


class UserCreate(UserBase):
    password: str


class User(UserBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str
    external_id: str | None = None
    external_auth: str | None = None

    received_messages: list["MessageRecipient"] = Relationship(back_populates='recipient',
                                                     sa_relationship_kwargs= {"foreign_keys": "[MessageRecipient.recipient_id]"})
    sent_messages: list["Message"] = Relationship(back_populates='sender', # type: ignore
                                                  sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"})
    tasks: list["Task"] = Relationship(back_populates='task_owner', # type: ignore
                                      sa_relationship_kwargs={"foreign_keys": "Task.task_owner_id"})

class UserUpdate(SQLModel):
    email: EmailStr | None = None
    name: str | None = None
    role: RoleEnum | None = None
    password: str | None = None


class UserPublic(UserBase):
    id: int
