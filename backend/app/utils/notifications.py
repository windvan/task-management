from ..schemas.message import Message, MessageRecipient
from ..schemas.task import Task
from ..schemas.enums import MessageCategoryEnum, MessageSeverityEnum
from sqlmodel import Session

from ..database.db import engine
from datetime import datetime,timedelta,timezone



WATCHING_FIELDS = ['task_status',
                   'task_progress',
                   'expected_delivery_date']


def create_task_notification(task: dict, updates: dict, current_user_id: int):
    updated_watching_fields = {}
    for field in WATCHING_FIELDS:
        if field in updates:
            if field == 'task_status':
                updated_watching_fields[field] = updates[field].value
            elif field == 'task_progress':
                updated_watching_fields[field] = updates[field].value
            elif field == 'expected_delivery_date':

                updated_watching_fields[field] = updates[field].astimezone(
                    timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
            else:
                updated_watching_fields[field] = updates[field]
    
    # updated_watching_fields = {
    #     field: updates[field] for field in WATCHING_FIELDS if field in updates}
    if not updated_watching_fields:
        return

    session = Session(engine)

    try:
        content = f"The following fields of task '{task.project_name}_{task.task_name}' has been updated on {task.updated_at.strftime("%Y-%m-%d")}:\n {updated_watching_fields}"
        # Create message for task update,to portfolio and task owner
        portfolio_contact_id = session.get(Task, task.id).project.portfolio_contact_id
        recipient_ids = [portfolio_contact_id, current_user_id]
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
        session.commit()
    finally:
        session.close()


def create_comment_notification(task: dict, updates: dict, current_user_id: int):
    pass
