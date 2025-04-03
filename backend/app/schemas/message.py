from sqlmodel import Field, Enum as dbEnum, Relationship, Column, DateTime
from pydantic import field_validator
from datetime import datetime
from ..database.database import AutoFieldMixin, SQLModel
from .enums import MessageSeverityEnum, MessageCategoryEnum
from ..utils.functions import date_to_utc


class Message(SQLModel, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sender_id: int | None = Field(default=None, foreign_key="user.id")
    category: MessageCategoryEnum = Field(sa_column=dbEnum(MessageCategoryEnum))
    content: str
    severity:  MessageSeverityEnum = Field(
        default=MessageSeverityEnum.Info, sa_column=dbEnum(MessageSeverityEnum))

    sender: "User" = Relationship(back_populates="sent_messages",  # type: ignore
                                  sa_relationship_kwargs={"foreign_keys": "Message.sender_id"}
                                  )
    recipients: list["MessageRecipient"] = Relationship(back_populates="message")


class MessageRecipient(SQLModel, AutoFieldMixin, table=True):
    __tablename__ = "message_recipient_rel"
    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="message.id")
    recipient_id: int = Field(foreign_key="user.id")
    is_read: bool = Field(default=False)
    read_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    message: Message = Relationship(back_populates="recipients")
    recipient: "User" = Relationship(back_populates="received_messages", sa_relationship_kwargs={  # type: ignore
                                     "foreign_keys": "MessageRecipient.recipient_id"})

    @field_validator('read_at')
    @classmethod
    def date_field_validator(cls, v):
        return date_to_utc(v)
