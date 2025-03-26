from fastapi import APIRouter, status, HTTPException, UploadFile, Form
from uuid import uuid4
from pathlib import Path
from sqlmodel import select

from ..schemas.gap import Gap
from ..schemas.task import Task

from ..schemas.user import User, UserCreate, UserPublic, UserUpdate
from ..utils.functions import get_password_hash
from ..utils.dependencies import SessionDep, TokenDep
from ..config import settings

router = APIRouter(prefix='/gaps', tags=["Gap"])


@router.get('/')
def get_all_gaps(session: SessionDep):

    db_gaps = session.exec(select(Gap)).all()

    return db_gaps


@router.get('/{gap_id}')
def get_all_gaps(gap_id: int, session: SessionDep):
    db_gap = session.get(Gap, gap_id)
    if not db_gap:
        raise HTTPException(status_code=404, detail="Gap not found")
    return db_gap


@router.post("/", status_code=status.HTTP_200_OK)
async def create_gap(session: SessionDep, task_id: int, file: UploadFile,  gap_detail: str = Form()):
    # create gap without associated task is not allowed
    # get gap img path
    gap_dir = Path(__file__).parent.parent / settings.STATIC_ROOT/settings.STATIC_GAP_FOLDER
    # assure existance of target dir
    gap_dir.mkdir(parents=True, exist_ok=True)
    # find related task
    db_task = session.get(Task, task_id)

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # generate random file name(uuid) with full path
    snapshot_filename = f"{uuid4()}{Path(file.filename).suffix}"
    snapshot_path = gap_dir / snapshot_filename
    # save file
    with snapshot_path.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # save gap detail (snapshot_url is relative to static file path)
    db_gap = Gap.model_validate_json(gap_detail)
    db_gap.sqlmodel_update({"snapshot_url": settings.STATIC_GAP_FOLDER+'/'+snapshot_filename})
    session.add(db_gap)
    session.commit()
    # update task.gap_id
    db_task.gap_id = db_gap.id
    session.add(db_task)
    session.commit()

    session.refresh(db_gap)
    return db_gap


@router.delete("/{gap_id}", status_code=status.HTTP_200_OK)
async def delete_gap(gap_id: int, session: SessionDep, task_id: int | None = None):

    db_gap = session.get(Gap, gap_id)
    if not db_gap:
        raise HTTPException(status_code=404, detail="Gap not found")

    # remove relationship
    if task_id:
        db_task = session.get(Task, task_id)
        db_gap.tasks.remove(db_task)
    # if gap has no related task, delete the task
    if not db_gap.tasks:
        session.delete(db_gap)
        session.commit()
        # remove image
        img_path = Path(__file__).parent.parent / settings.STATIC_ROOT / db_gap.snapshot_url
        img_path.unlink()

    return {"message": "Gap deleted successfully"}
