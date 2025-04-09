from sqlmodel import Field, Relationship, Enum as dbEnum, Column, JSON

from ..database.db import AutoFieldMixin, SQLModel
from .enums import CommentSeverityEnum


class ProjectComment(SQLModel, AutoFieldMixin, table=True):
    __tablename__ = 'project_comment'
    id: int = Field(default=None, primary_key=True)
    project_id: int | None = Field(default=None, foreign_key='project.id')
    parent_id: int | None = Field(foreign_key='project_comment.id')
    content: str  # quill delta array
    mentions: list[str] | None = Field(default=None, sa_column=Column(JSON))  # "[1,2,3]"
    severity: CommentSeverityEnum = Field(
        default=CommentSeverityEnum.Info, sa_column=dbEnum(CommentSeverityEnum))

    project: "Project" = Relationship(back_populates="comments")  # type: ignore


class TaskComment(SQLModel, AutoFieldMixin, table=True):
    __tablename__ = 'task_comment'
    id: int = Field(default=None, primary_key=True)
    task_id: int | None = Field(foreign_key='task.id')
    parent_id: int | None = Field(default=None, foreign_key='task_comment.id')
    content: str  # quill delta array
    mentions: list[str] | None = Field(default=None, sa_column=Column(JSON))  # "[1,2,3]"
    severity: CommentSeverityEnum = Field(
        default=CommentSeverityEnum.Info, sa_column=dbEnum(CommentSeverityEnum))

    task: "Task" = Relationship(back_populates="comments")  # type: ignore
