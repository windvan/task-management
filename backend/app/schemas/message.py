from sqlmodel import Field, Enum as dbEnum, Relationship, Column, DateTime
from pydantic import model_validator
from sqlmodel import SQLModel
from datetime import datetime,timezone
from ..database.db import AutoFieldMixin, SQLModel
from .enums import MessageSeverityEnum, MessageCategoryEnum



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
    read_at: datetime | None = None

    message: Message = Relationship(back_populates="recipients")
    recipient: "User" = Relationship(back_populates="received_messages", sa_relationship_kwargs={  # type: ignore
                                     "foreign_keys": "MessageRecipient.recipient_id"})

    # generate read_at if is_read set to True
    @model_validator(mode='after')
    def set_read_at(self):
        if self.is_read:
            self.read_at = datetime.now(timezone.utc)
        return self
