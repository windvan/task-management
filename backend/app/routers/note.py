from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlmodel import select

from ..schemas.user import User

from ..schemas.note import Note, NoteCreate, NotePublic
from ..schemas.task import Task
from ..schemas.project import Project
from ..utils.dependencies import SessionDep

router = APIRouter(prefix='/notes', tags=["Note"])


@router.post("/")
def create_note(note_create: NoteCreate, session: SessionDep):
    db_note = Note.model_validate(note_create)
    session.add(db_note)
    session.commit()
    new_note = session.exec(
        select(Note.__table__.columns, User.name.label('created_by_name'))
        .join(User, Note.created_by == User.id)
        .where(Note.id == db_note.id)).mappings().one()
    return new_note


@router.get("/{note_id}")
def get_note(note_id: int, session: SessionDep):
    db_note = session.exec(
        select(Note.__table__.columns, User.name.label('created_by_name'))
        .join(User, Note.created_by == User.id)
        .where(Note.id == note_id)).mappings().one()
    return db_note


@router.get("/task/{task_id}")
def get_notes(session: SessionDep, response: Response, task_id: int):
    response.headers['cache-control'] = 'max-age=604800'  # 7 days
    if task_id:
        db_task = session.get(Task, task_id)
        project_id = db_task.project_id
        project_notes = session.exec(
            select(Note.__table__.columns, User.name.label('created_by_name'))
            .join(User, Note.created_by == User.id)
            .where(Note.project_id == project_id)
            .order_by(Note.updated_at.desc())
        ).mappings().all()
        task_notes = session.exec(
            select(Note.__table__.columns, User.name.label('created_by_name'))
            .join(User, Note.created_by == User.id)
            .where(Note.task_id == task_id)
            .order_by(Note.updated_at.desc())).mappings().all()
        return {
            "project_notes": project_notes,
            "task_notes": task_notes
        }


@router.get("/project/{project_id}")
def get_notes(session: SessionDep, response: Response,  project_id: int):
    response.headers['cache-control'] = 'max-age=604800'  # 7 days

    if project_id:
        db_project = session.get(Project, project_id)
        task_id_list = [task.id for task in db_project.tasks]
        project_notes = session.exec(
            select(Note.__table__.columns, User.name.label('created_by_name'))
            .join(User, Note.created_by == User.id)
            .where(Note.project_id == project_id)).mappings().all()
        task_notes = session.exec(
            select(Note.__table__.columns, User.name.label('created_by_name'))
            .join(User, Note.created_by == User.id).where(
                Note.task_id.in_(task_id_list))).mappings().all()
        return {
            "project_notes": project_notes,
            "task_notes": task_notes
        }

    return None


@router.patch('/{note_id}')
def update_note(session: SessionDep, note_id: int, updates: dict):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="note not found")
    db_note.sqlmodel_update(updates)
    session.add(db_note)
    session.commit()
    new_note = session.exec(
        select(Note.__table__.columns, User.name.label('created_by_name'))
        .join(User, Note.created_by == User.id)
        .where(Note.id == db_note.id)).mappings().one()
    return new_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="note not found")
    session.delete(db_note)
    session.commit()
    return {"message": "note deleted successfully"}
