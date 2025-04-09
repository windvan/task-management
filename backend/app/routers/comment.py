from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlmodel import select

from ..schemas.user import User

from ..schemas.comment import ProjectComment,TaskComment
from ..schemas.task import Task
from ..schemas.project import Project
from ..utils.dependencies import SessionDep

router = APIRouter(prefix='/comments', tags=["Comment"])


@router.post("/project")
def create_project_comment(proj_comment: dict, session: SessionDep):
    db_comment = ProjectComment.model_validate(proj_comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)

    return db_comment


@router.post("/task")
def create_task_comment(task_comment: dict, session: SessionDep):
    db_comment = TaskComment.model_validate(task_comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)

    return db_comment


@router.get("/all")
def get_all_comments(session: SessionDep):
    db_comments = session.exec(
        select(ProjectComment).union_all(select(TaskComment))).all()
        
    return db_comments


@router.get("/task/{task_id}")
def get_task_comments(task_id: int, session: SessionDep):
    db_comments = session.exec(
        select(TaskComment).where(TaskComment.task_id == task_id)).all()
    return db_comments

@router.get("/project/{project_id}")
def get_project_comments(project_id: int, session: SessionDep):
    db_comments = session.exec(
        select(ProjectComment).where(ProjectComment.project_id == project_id)).all()
    return db_comments

@router.patch("/project/{comment_id}")
def update_project_comment(comment_id: int, updates: dict, session: SessionDep):
    db_comment = session.get(ProjectComment, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="comment not found")
    db_comment.sqlmodel_update(updates)
    session.add(db_comment)
    session.commit()
    return db_comment

@router.patch("/task/{comment_id}")
def update_task_comment(comment_id: int, updates: dict, session: SessionDep):
    db_comment = session.get(TaskComment, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="comment not found")
    db_comment.sqlmodel_update(updates)
    session.add(db_comment)
    session.commit()
    return db_comment