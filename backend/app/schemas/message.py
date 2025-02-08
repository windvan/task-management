from sqlmodel import Field, Enum as dbEnum, Relationship
from datetime import datetime
from ..database.database import SQLModel
from .enums import MessageSeverityEnum


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sender_id: int | None = Field(default=None, foreign_key="user.id")
    content: str
    severity:  MessageSeverityEnum = Field(
        default=MessageSeverityEnum.Info, sa_column=dbEnum(MessageSeverityEnum))

    sender: "User" = Relationship(back_populates="sent_messages", # type: ignore
                                  sa_relationship_kwargs={"foreign_keys": "Message.sender_id"}
                        )
    recipients: list["MessageRecipient"] = Relationship(back_populates="message")


class MessageRecipient(SQLModel, table=True):
    __tablename__ = "message_recipient_rel"
    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="message.id")
    recipient_id: int = Field(foreign_key="user.id")
    is_read: bool = Field(default=False)
    read_at: datetime | None = Field(default=None)

    message: Message = Relationship(back_populates="recipients")
    recipient: "User" = Relationship(back_populates="received_messages", sa_relationship_kwargs={ # type: ignore
                                     "foreign_keys": "MessageRecipient.recipient_id"})
