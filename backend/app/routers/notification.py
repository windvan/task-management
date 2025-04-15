from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from ..schemas.message import Message, MessageRecipient
from datetime import datetime, timezone,timedelta
from sqlalchemy import func

from ..utils.dependencies import SessionDep
from ..schemas import Task, Project

router = APIRouter(prefix='/notifications', tags=["Notification"])


@router.get('/reminders/')
def get_task_reminder(session: SessionDep):
    user_id = session._current_user_id

    stmt = select(
        Task.task_name,
        Task.expected_delivery_date,
        Project.project_name,
        func.datediff(
            Task.expected_delivery_date,
            func.utc_timestamp()).label('days_remaining')
    ).join(
        Project, Project.id == Task.project_id
    ).where(
        Task.expected_delivery_date <= datetime.now(timezone.utc) + timedelta(days=30)
    ).where(
        Task.task_owner_id == user_id
    ).where(
        Task.task_status == "Go"
    ).order_by(Task.expected_delivery_date)

    tasks_to_remind = session.exec(stmt).mappings().all()
    return tasks_to_remind


@router.get('/updates/')
def get_task_message(session: SessionDep):
    user_id = session._current_user_id

    stmt = select(Message.severity, Message.content, MessageRecipient.id.label("msg_recp_id"), MessageRecipient.is_read).join(MessageRecipient, MessageRecipient.message_id == Message.id).where(
        MessageRecipient.recipient_id == user_id,
    ).order_by(MessageRecipient.is_read, Message.created_at.desc())
    updates = session.exec(stmt.where(
        Message.category == "Update"
    )).mappings().all()

    return updates


@router.get('/messages/')  # mentions
def get_task_message(session: SessionDep):
    user_id = session._current_user_id

    stmt = select(Message.severity, Message.content, MessageRecipient.id.label("msg_recp_id"), MessageRecipient.is_read).join(MessageRecipient, MessageRecipient.message_id == Message.id).where(
        MessageRecipient.recipient_id == user_id,
    ).order_by(MessageRecipient.is_read, Message.created_at.desc())

    mentions = session.exec(stmt.where(
        Message.category == "Mention"
    )).mappings().all()

    return mentions
