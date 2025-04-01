from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlmodel import select

from ..schemas.note import Note, NoteCreate, NotePublic
from ..schemas.task import Task
from ..schemas.project import Project
from ..utils.dependencies import SessionDep

router = APIRouter(prefix='/notes', tags=["Note"])


@router.post("/", response_model=NotePublic, status_code=status.HTTP_200_OK)
def create_note(note_create: NoteCreate, session: SessionDep):
    db_note = Note.model_validate(note_create)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@router.get("/{note_id}", response_model=NotePublic)
def get_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="note not found")
    return db_note


@router.get("/tasks/{task_id}")
def get_notes(session: SessionDep, response: Response, task_id: int):
    response.headers['cache-control'] = 'max-age=604800' # 7 days
    if task_id:
        db_task = session.get(Task, task_id)
        project_id = db_task.project_id
        project_notes = session.exec(select(Note).where(
            Note.project_id == project_id)).all()
        task_notes = session.exec(
            select(Note).where(Note.task_id == task_id)).all()
        return {
            "project_notes": project_notes,
            "task_notes": task_notes
        }

    


@router.get("/projects/{project_id}")
def get_notes(session: SessionDep, response: Response,  project_id: int ):
    response.headers['cache-control'] = 'max-age=604800'  # 7 days
    
    if project_id:
        db_project = session.get(Project, project_id)
        task_id_list = [task.id for task in db_project.tasks]
        project_notes = session.exec(select(Note).where(
            Note.project_id == project_id)).all()
        task_notes = session.exec(select(Note).where(
            Note.task_id.in_(task_id_list))).all()
        return {
            "project_notes": project_notes,
            "task_notes": task_notes
        }

    return None


@router.get("/{note_id}", response_model=NotePublic)
# @router.patch('/{note_id}', response_model=NotePublic)
# def update_note(note_id: int, note_update: NoteUpdate, session: SessionDep):
#     db_note = session.get(Note, note_id)
#     if not db_note:
#         raise HTTPException(status_code=404, detail="note not found")
#     note_data = note_update.model_dump(exclude_unset=True)
#     db_note.sqlmodel_update(note_data)
#     session.add(db_note)
#     session.commit()
#     session.refresh(db_note)
#     return db_note
@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="note not found")
    session.delete(db_note)
    session.commit()
    return {"message": "note deleted successfully"}
