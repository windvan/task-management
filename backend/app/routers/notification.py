from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from ..schemas.message import Message, MessageRecipient
from datetime import datetime, timezone, timedelta
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

    stmt = select(Message.severity, Message.content, Message.category,MessageRecipient.id.label("msg_recp_id"), MessageRecipient.is_read).join(MessageRecipient, MessageRecipient.message_id == Message.id).where(
        MessageRecipient.recipient_id == user_id,
    ).order_by(MessageRecipient.is_read, Message.created_at.desc())
    updates = session.exec(stmt.where(
        Message.category == "Update"
    )).mappings().all()

    return updates


@router.get('/messages/')  # mentions
def get_task_message(session: SessionDep):
    user_id = session._current_user_id

    stmt = select(Message.severity, Message.content, Message.category, MessageRecipient.id.label("msg_recp_id"), MessageRecipient.is_read).join(MessageRecipient, MessageRecipient.message_id == Message.id).where(
        MessageRecipient.recipient_id == user_id,
    ).order_by(MessageRecipient.is_read, Message.created_at.desc())

    mentions = session.exec(stmt.where(
        Message.category == "Mention"
    )).mappings().all()

    return mentions


# @router.patch("/read/{msg_recp_id}")
# def update_message(msg_recp_id: int, updates: dict, session: SessionDep = SessionDep):
#     # mark updates and notification as read
#     db_msg_recipient = session.get(MessageRecipient, msg_recp_id)
#     if not db_msg_recipient:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MessageRecipient not found")
#     # Update the message fields
#     db_msg_recipient.sqlmodel_update(updates, update={"read_at": datetime.now(
#         timezone.utc) if updates.get("is_read") else None})

#     session.add(db_msg_recipient)
#     session.commit()

#     return {"message": "Message marked as read", "updated_count": 1}


@router.patch("/read")
def batch_read_message(msg_recp_ids: int | list[int], session: SessionDep = SessionDep):
    # mark updates and notification as read
    if not msg_recp_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No message IDs provided")

    if isinstance(msg_recp_ids, int):
        db_msg_recipient = session.get(MessageRecipient, msg_recp_ids)
        db_msg_recipient.sqlmodel_update({"is_read": True, "read_at": datetime.now(timezone.utc)})
        session.add(db_msg_recipient)
        session.commit()
        return {"message": "Messages marked as read", "updated_count": 1}

    else:
        stmt = select(MessageRecipient).where(MessageRecipient.id.in_(msg_recp_ids))
        db_msg_recps = session.exec(stmt).all()
        for msg_recp in db_msg_recps:
            msg_recp.sqlmodel_update({"is_read": True, "read_at": datetime.now(timezone.utc)})
            session.add(msg_recp)
        session.commit()
        return {"message": "Messages marked as read", "updated_count": len(db_msg_recps)}


@router.patch("/unread")
def batch_read_message(msg_recp_ids: int | list[int], session: SessionDep = SessionDep):
    # mark updates and notification as read
    if not msg_recp_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No message IDs provided")

    if isinstance(msg_recp_ids, int):
        db_msg_recipient = session.get(MessageRecipient, msg_recp_ids)
        db_msg_recipient.sqlmodel_update({"is_read": False, "read_at": None})
        session.add(db_msg_recipient)
        session.commit()
        return {"message": "Messages marked as read", "updated_count": 1}

    else:
        stmt = select(MessageRecipient).where(MessageRecipient.id.in_(msg_recp_ids))
        db_msg_recps = session.exec(stmt).all()
        for msg_recp in db_msg_recps:
            msg_recp.sqlmodel_update({"is_read": False, "read_at": None})
            session.add(msg_recp)
        session.commit()
        return {"message": "Messages marked as read", "updated_count": len(db_msg_recps)}
