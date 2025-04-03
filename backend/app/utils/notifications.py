from ..schemas.message import Message, MessageRecipient
from ..schemas.enums import MessageCategoryEnum, MessageSeverityEnum
from sqlmodel import Session
from typing import List
from ..database.database import UserAwareSession, engine


async def create_task_update_message(
    sender_id: int,
    recipient_ids: List[int],
    task_name: str,
    field_name: str,
    new_value: str,
    category: MessageCategoryEnum = MessageCategoryEnum.Update,
    severity: MessageSeverityEnum = MessageSeverityEnum.Info
):
    """Create a notification message for task updates"""
    # Create new session for background task
    session = UserAwareSession(engine)
    try:
        content = f"Task '{task_name}' has been updated: {field_name} changed to {new_value}"

        message = Message(
            sender_id=sender_id,
            category=category,
            content=content,
            severity=severity
        )

        session.add(message)
        session.flush()

        # Create message recipients
        for recipient_id in recipient_ids:
            message.recipients.append(MessageRecipient(
                message_id=message.id,
                recipient_id=recipient_id
            ))

        session.commit()
    finally:
        session.close()
