from ..schemas.message import Message, MessageRecipient
from ..schemas.task import Task
from ..schemas.enums import MessageCategoryEnum, MessageSeverityEnum
from sqlmodel import Session

from ..database.database import engine


WATCHING_FIELDS = ['task_status',
                   'task_progress',
                   'expected_delivery_date']


def create_task_notification(task: dict, updates: dict, current_user_id: int):
    print("create_task_notification", '\n\n\n\n\n\n', updates)

    updated_watching_fields = {
        field: updates[field] for field in WATCHING_FIELDS if field in updates}
    if not updated_watching_fields:
        return

    session = Session(engine)

    try:
        content = f"The following fields of task '{task.project_name}_{task.task_name}' has been updated:\n {updates}"
        # Create message for task update,to portfolio and task owner
        recipient_ids = [task.project.portfolio_contact_id, current_user_id]
        message = Message(
            sender_id=current_user_id,
            category=MessageCategoryEnum.Update,
            content=content,
            severity=MessageSeverityEnum.Info
        )

        message.recipients = [
            MessageRecipient(
                recipient_id=recipient_id
            ) for recipient_id in recipient_ids
        ]

        session.add(message)
        session.flush()
    finally:
        session.close()
