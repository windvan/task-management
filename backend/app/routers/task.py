from fastapi import APIRouter, Form, Query, status, HTTPException, UploadFile, Body
from sqlalchemy import or_, and_
from sqlmodel import select, delete, SQLModel
from sqlalchemy.orm import joinedload, selectinload, load_only
from pathlib import Path
from uuid import uuid4

from app.schemas.product import Product

from ..schemas.task import Task, TaskCreate, TaskPublic, TaskUpdate, TaskLibrary, TaskLibraryCreate
from ..schemas.project import Project
from ..schemas.user import User
from ..schemas.cro import Cro
from ..schemas.gap import Gap, GapCreate
from ..schemas.sample import Sample, SamplePublic
from ..utils.dependencies import SessionDep, TokenDep
from ..schemas.enums import SampleStatusEnum
from ..config import settings


router = APIRouter(prefix='/tasks', tags=["Task"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate | list[TaskCreate], session: SessionDep):
    if isinstance(task_create, list):
        # 处理多条记录
        db_tasks = []
        for task in task_create:
            db_tasks.append(Task.model_validate(task))

        session.add_all(db_tasks)
        session.commit()

        task_id_list = [task.id for task in db_tasks]

        stmt = select(Task.__table__.columns,
                      Project.project_name,
                      Project.project_status,
                      Product.stage.label('product_stage'),
                      User.name.label('task_owner_name'),
                      Cro.cro_name,
                      Sample.sample_status).outerjoin(
            Project, Project.id == Task.project_id).outerjoin(
            Product, Product.id == Project.product_id).outerjoin(
            User, User.id == Task.task_owner_id).outerjoin(
            Cro, Cro.id == Task.cro_id).outerjoin(
            Sample, Sample.id == Task.sample_id).where(Task.id.in_(task_id_list))

        db_tasks = session.exec(stmt).mappings().all()
        return db_tasks

    else:
        # 处理单条记录
        db_task = Task.model_validate(task_create)

        session.add(db_task)
        session.commit()

        stmt = select(Task.__table__.columns,
                      Project.project_name,
                      Project.project_status,
                      Product.stage.label('product_stage'),
                      User.name.label('task_owner_name'),
                      Cro.cro_name,

                      Sample.sample_status).outerjoin(
            Project, Project.id == Task.project_id).outerjoin(
            Product, Product.id == Project.product_id).outerjoin(
            User, User.id == Task.task_owner_id,).outerjoin(
            Cro, Cro.id == Task.cro_id).outerjoin(
            Sample, Sample.id == Task.sample_id).where(Task.id == db_task.id)

        db_task = session.exec(stmt).mappings().first()
        return db_task


@router.get("/")
def get_tasks(session: SessionDep):

    stmt = select(Task.__table__.columns,
                  Project.project_name,
                  Project.project_status,
                  Product.stage.label('product_stage'),
                  User.name.label('task_owner_name'),
                  Cro.cro_name,

                  Sample.sample_status).outerjoin(
        Project, Project.id == Task.project_id).outerjoin(
        Product, Product.id == Project.product_id).outerjoin(
        User, User.id == Task.task_owner_id,).outerjoin(
        Cro, Cro.id == Task.cro_id).outerjoin(
        Sample, Sample.id == Task.sample_id)
# .where(User.id == user_id)
    db_tasks = session.exec(stmt).mappings().all()

    return db_tasks


@router.get('/task-columns')
def get_task_columns(user_id: SessionDep):
    stmt = select(Task.__table__.columns,
                  Project.project_name,
                  User.name.label('task_owner_name'),
                  Cro.cro_name,

                  Sample.sample_status)
    return [col.name for col in stmt.selected_columns]


@router.get('/search')
def search_tasks(session: SessionDep,  query: str = "", sample_id: int = None):

    search_pattern = f"%{query}%"
    conditions = and_(
        or_(
            Product.trade_name.ilike(search_pattern),
            Product.internal_name.ilike(search_pattern),
            Task.task_name.ilike(search_pattern),  # 不区分大小写的模糊匹配
            Task.tags.ilike(search_pattern)),
        Task.task_owner_id == session._current_user_id,
        or_(Task.sample_id.is_(None), Task.sample_id != sample_id) if sample_id else True
    )

    stmt = select(
        Task.id,
        Task.task_name,
        Task.tags,
        Product.internal_name.label("product_internal_name"),
        Product.trade_name.label("product_trade_name"),

    ).outerjoin(Task.project).outerjoin(Project.product).outerjoin(Task.task_owner).where(conditions)

    results = session.exec(stmt).mappings().all()
    # 转换为字典格式
    return results


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task_id: int, session: SessionDep):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")
    return db_task


# update one task with modified fields
@router.patch('/{task_id}')
def update_task(task_id: int, fields_to_update: dict, session: SessionDep):

    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail=f"Task with id {
                            task_id} not found")

    # task_update = task_data.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(fields_to_update)
    session.add(db_task)
    session.commit()

    # return task and related fields
    stmt = select(Task.__table__.columns,
                  Project.project_name,
                  Project.project_status,
                  Product.stage.label('product_stage'),
                  User.name.label('task_owner_name'),
                  Cro.cro_name,
                  Sample.sample_status).outerjoin(
        Project, Project.id == Task.project_id).outerjoin(
        Product, Product.id == Project.product_id).outerjoin(
        User, User.id == Task.task_owner_id).outerjoin(
        Cro, Cro.id == Task.cro_id).outerjoin(
        Sample, Sample.id == Task.sample_id).where(Task.id == task_id)

    task = session.exec(stmt).mappings().first()
    return task


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_task(session: SessionDep, task_ids: int | list[int] = Body()):
    if isinstance(task_ids, list):
        # 批量删除多条记录
        stmt = delete(Task).where(Task.id.in_(task_ids))
        result = session.exec(stmt)
        deleted_count = result.rowcount

        if deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="No tasks found with the provided ids")

    else:
        # 删除单条记录
        db_task = session.get(Task, task_ids)
        if not db_task:
            raise HTTPException(status_code=404, detail=f"Task with id {
                                task_ids} not found")
        session.delete(db_task)
        deleted_count = 1

    session.commit()
    return {"message": f"{deleted_count} task(s) deleted successfully"}


@router.post("/task-library", status_code=status.HTTP_201_CREATED)
def create_task_library_item(item_create: TaskLibraryCreate, session: SessionDep):
    db_library_item = Task.model_validate(item_create)
    session.add(db_library_item)
    session.commit()
    session.refresh(db_library_item)
    return db_library_item


@router.get('/task-name/search')
def search_tasks(session: SessionDep, query: str = ""):

    search_pattern = f"%{query}%"
    conditions = or_(
        TaskLibrary.task_category.ilike(search_pattern),
        TaskLibrary.task_name.ilike(search_pattern),
    )

    stmt = select(
        TaskLibrary.id,
        TaskLibrary.task_category,
        TaskLibrary.task_name.label('task_name')).where(conditions)

    results = session.exec(stmt).mappings().all()
    # 转换为字典格式
    return results
