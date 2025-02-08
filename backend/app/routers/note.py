from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import select

from ..schemas.note import Note, NoteCreate, NotePublic
from ..utils.dependencies import SessionDep

router = APIRouter(prefix='/notes', tags=["Note"])


@router.post("/", response_model=NotePublic, status_code=status.HTTP_201_CREATED)
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


@router.get("/", response_model=list[NotePublic])
def get_notes(session: SessionDep):
    db_notes = session.exec(select(Note)).all()
    return db_notes


# @router.patch('/{note_id}', response_model=NotePublic)
# def update_note(note_id: int, note_update: NoteUpdate, session: SessionDep, token: TokenDep):
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
