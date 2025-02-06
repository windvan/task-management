from sqlmodel import Field, Enum as dbEnum, Relationship
from datetime import time
from ..database import SQLModel
from .user import User
from .enums import MessageSeverityEnum


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    severity:  MessageSeverityEnum = Field(
        default=MessageSeverityEnum.Info, sa_column=dbEnum(MessageSeverityEnum))
    # created_at:datatime.time
    # cteated_by:User

    sender: User = Relationship(back_populates="sent_messages")
    recipients: list["MessageRecipient"] = Relationship(back_populates="message")


class MessageRecipient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="message.id")
    recipient_id: int = Field(foreign_key="user.id")
    read_at: time | None = Field(default=None)

    message: Message = Relationship(back_populates="recipients")
    recipient: User = Relationship(back_populates="received_messages")
