from sqlmodel import Field, Relationship, Enum as dbEnum
from pydantic import model_validator
from sqlalchemy import CheckConstraint


from ..database.database import SQLModel
from .enums import NoteSeverityEnum


class TaskNoteRelationship(SQLModel, table=True):
    __tablename__ = "task_note_rel"
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    note_id: int = Field(foreign_key="note.id", primary_key=True)


class ProjectNoteRelationship(SQLModel, table=True):
    __tablename__ = "project_note_rel"
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    note_id: int = Field(foreign_key="note.id", primary_key=True)


class Note(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_id: int | None = Field(default=None, foreign_key='project.id')
    task_id: int | None = Field(default=None, foreign_key='task.id')
    content: str
    tags: str | None = None
    severity: NoteSeverityEnum = Field(
        default=NoteSeverityEnum.Info, sa_column=dbEnum(NoteSeverityEnum))

    project: "Project" = Relationship(  # type: ignore
        back_populates="notes", link_model=ProjectNoteRelationship)
    task: "Task" = Relationship(  # type: ignore
        back_populates="notes", link_model=TaskNoteRelationship)

    __table_args__ = (
        CheckConstraint(
            '(project_id IS NULL AND task_id IS NOT NULL) OR (project_id IS NOT NULL AND task_id IS NULL)',
            name='check_project_or_task'
        ),
    )

    @model_validator(mode='after')
    def check_project_or_task(cls, values):
        project_id = values.project_id
        task_id = values.task_id
        if (project_id is None and task_id is None) or (project_id is not None and task_id is not None):
            raise ValueError("Either project_id or task_id must be set, but not both")
        return values


class NoteCreate(SQLModel):
    pass


class NotePublic(SQLModel):
    pass