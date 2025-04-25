from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from ..schemas.message import Message, MessageRecipient
from datetime import datetime, timezone

from ..utils.dependencies import SessionDep

router = APIRouter(prefix='/messages', tags=["Message"])


@router.patch("/read/{msg_recp_id}")
def update_message(msg_recp_id: int, updates: dict, session: SessionDep = SessionDep):

    db_msg_recipient = session.get(MessageRecipient, msg_recp_id)
    if not db_msg_recipient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MessageRecipient not found")
    # Update the message fields
    db_msg_recipient.sqlmodel_update(updates, update={"read_at": datetime.now(
        timezone.utc) if updates.get("is_read") else None})

    session.add(db_msg_recipient)
    session.commit()

    return {"message": "Message marked as read", "updated_count": 1}


@router.patch("/batch-read")
def batch_read_message(msg_recp_ids: list[int], session: SessionDep = SessionDep):
    if not msg_recp_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No message IDs provided")

    stmt = select(MessageRecipient).where(MessageRecipient.id.in_(msg_recp_ids))

    db_msg_recps = session.exec(stmt).all()

    for msg_recp in db_msg_recps:
        msg_recp.sqlmodel_update({"is_read": True, "read_at": datetime.now(timezone.utc)})
        session.add(msg_recp)

    session.commit()
    return {"message": "Messages marked as read", "updated_count": len(db_msg_recps)}
