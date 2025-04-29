from sqlmodel import Field, Relationship, Enum as dbEnum, Column, Text, JSON

from ..database.db import AutoFieldMixin, SQLModel
from .enums import CommentSeverityEnum
from datetime import datetime
from ..schemas import User, Task, Project


class ProjectComment(SQLModel, AutoFieldMixin, table=True):
    __tablename__ = 'project_comment'

    id: int = Field(default=None, primary_key=True)
    project_id: int | None = Field(default=None, foreign_key='project.id')
    parent_id: int | None = Field(foreign_key='project_comment.id')
    rich_text: str = Field(sa_column=Column(Text))  # html format
    plain_text: str = Field(sa_column=Column(Text))  # plain text
    mentions: list[int] | None = Field(default=None, sa_column=Column(JSON))  # "[1,2,3]"
    severity: CommentSeverityEnum | None = Field(
        default=CommentSeverityEnum.Info, sa_column=dbEnum(CommentSeverityEnum))

    project: "Project" = Relationship(back_populates="comments")  # type: ignore
    children: list["ProjectComment"] = Relationship()
    creater: "User" = Relationship(sa_relationship_kwargs={
                                   "foreign_keys": "ProjectComment.created_by"})


class TaskComment(SQLModel, AutoFieldMixin, table=True):
    __tablename__ = 'task_comment'

    id: int = Field(default=None, primary_key=True)
    task_id: int | None = Field(default=None, foreign_key='task.id')
    parent_id: int | None = Field(foreign_key='task_comment.id')
    rich_text: str = Field(sa_column=Column(Text))  # html format
    plain_text: str = Field(sa_column=Column(Text))   # plain text
    mentions: list[int] | None = Field(default=None, sa_column=Column(JSON))  # "[1,2,3]"
    severity: CommentSeverityEnum | None = Field(
        default=CommentSeverityEnum.Info, sa_column=dbEnum(CommentSeverityEnum))

    task: "Task" = Relationship(back_populates="comments", sa_relationship_kwargs={
                                "foreign_keys": "TaskComment.task_id"})  # type: ignore
    children: list["TaskComment"] = Relationship(sa_relationship_kwargs={"foreign_keys": "TaskComment.parent_id"})
    creater: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "TaskComment.created_by"})


class ProjectCommentPublic(SQLModel):
    id: int
    project_id: int | None
    parent_id: int | None
    rich_text: str = Field(sa_column=Column(Text))  # html format
    plain_text: str = Field(sa_column=Column(Text))  # plain text
    mentions: list[int] | None
    severity: CommentSeverityEnum | None
    children: list["TaskComment"]
    created_by_name: str
    created_at: datetime


class TaskCommentPublic(SQLModel):
    id: int
    task_id: int | None
    parent_id: int | None
    rich_text: str = Field(sa_column=Column(Text))  # html format
    plain_text: str = Field(sa_column=Column(Text))  # plain text
    mentions: list[int] | None
    severity: CommentSeverityEnum | None
    children: list["TaskComment"]
    created_by_name: str
    created_at: datetime


class CommentsOut(SQLModel):
    project_comments: list[ProjectCommentPublic]
    task_comments: list[TaskCommentPublic]
