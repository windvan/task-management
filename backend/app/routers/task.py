from fastapi import APIRouter, Query, status, HTTPException, UploadFile, Body
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
from ..schemas.gap import Gap
from ..schemas.sample import Sample, SamplePublic
from ..utils.dependencies import SessionDep, TokenDep
from ..schemas.enums import SampleStatusEnum


router = APIRouter(prefix='/tasks', tags=["Task"])


@router.post("/", response_model=TaskPublic | list[TaskPublic], status_code=status.HTTP_201_CREATED)
def create_task(task_create: TaskCreate | list[TaskCreate], session: SessionDep, token: TokenDep):
    if isinstance(task_create, list):
        # 处理多条记录
        db_tasks = []
        for task in task_create:
            db_task = Task.model_validate(task)
            session.add(db_task)
            db_tasks.append(db_task)
        session.commit()
        for db_task in db_tasks:
            session.refresh(db_task)
        return db_tasks
    else:
        # 处理单条记录
        db_task = Task.model_validate(task_create)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@router.get("/")
def get_tasks(session: SessionDep, user_id: TokenDep):

    stmt = select(Task.__table__.columns,
                  Project.project_name,
                  User.name.label('task_owner_name'),
                  Cro.cro_name,
                  Gap.snapshot_url.label('gap_snapshot_url'),
                  Sample.sample_status).outerjoin(
        Project, Project.id == Task.project_id).outerjoin(
        User, User.id == Task.task_owner_id,).outerjoin(
        Gap, Gap.id == Task.gap_id).outerjoin(
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
                  Gap.snapshot_url.label('gap_snapshot_url'),
                  Sample.sample_status)
    return [col.name for col in stmt.selected_columns]


@router.get('/search')
def search_tasks(session: SessionDep, user_id: TokenDep, query: str = "", sample_id=None):
    search_pattern = f"%{query}%"
    conditions = and_(
        or_(
            Product.trade_name.ilike(search_pattern),
            Product.internal_name.ilike(search_pattern),
            Task.task_name.ilike(search_pattern),  # 不区分大小写的模糊匹配
            Task.tags.ilike(search_pattern)),
        Task.task_owner_id == user_id,
        Task.sample_id != sample_id if sample_id else True
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
def get_task(task_id: int, session: SessionDep, token: TokenDep):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")
    return db_task


# update one task with modified fields
@router.patch('/{task_id}')
def update_task(task_id: int, fields_to_update: dict, session: SessionDep, user_id: TokenDep):

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
                  User.name.label('task_owner_name'),
                  Cro.cro_name,
                  Gap.snapshot_url.label('gap_snapshot_url'),
                  Sample.sample_status).outerjoin(
        Project, Project.id == Task.project_id).outerjoin(
        User, User.id == Task.task_owner_id,).outerjoin(
        Gap, Gap.id == Task.gap_id).outerjoin(
        Cro, Cro.id == Task.cro_id).outerjoin(
        Sample, Sample.id == Task.sample_id).where(Task.id == task_id)

    task = session.exec(stmt).mappings().first()
    return task


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_task(task_ids: int | list[int], session: SessionDep, token: TokenDep):
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
def create_task_library_item(item_create: TaskLibraryCreate, session: SessionDep, token: TokenDep):
    db_library_item = Task.model_validate(item_create)
    session.add(db_library_item)
    session.commit()
    session.refresh(db_library_item)
    return db_library_item


@router.post("/gaps/{task_id}", status_code=status.HTTP_201_CREATED)
async def upload_gap(
    task_id: int,
    files: list[UploadFile],
    session: SessionDep, token: TokenDep
):
    # 获取保存图片的目录
    gap_dir = Path(__file__).parent.parent / "statics" / "images" / "gaps"

    # 确保目录存在
    gap_dir.mkdir(parents=True, exist_ok=True)

    # 查找对应的 task
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 保存图片并收集文件路径
    saved_paths = []
    for file in files:
        # 生成唯一文件名
        unique_filename = f"{uuid4()}{Path(file.filename).suffix}"
        file_path = gap_dir / unique_filename

        # 保存文件
        with file_path.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # 收集相对路径
        relative_path = f"images/gaps/{unique_filename}"
        saved_paths.append(relative_path)

    # 更新数据库中的 gap_snapshot 字段
    saved_paths_str = ",".join(saved_paths)

    db_task.gap_snapshot = db_task.gap_snapshot + "," + \
        saved_paths_str if db_task.gap_snapshot else saved_paths_str

    session.add(db_task)
    session.commit()

    return {"message": "Images uploaded successfully", "gap_snapshot": db_task.gap_snapshot}


@router.delete("/gaps/{task_id}", status_code=status.HTTP_200_OK)
async def delete_gap(task_id: int, session: SessionDep, token: TokenDep, gap_path: str):
    # 查找对应的 task
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    exits_path = db_task.gap_snapshot.split(",")
    exits_path.remove(gap_path)
    db_task.gap_snapshot = ",".join(exits_path) if exits_path else None

    file_path = Path(__file__).parent.parent / "statics" / gap_path
    if file_path.exists():
        file_path.unlink()

    session.add(db_task)
    session.commit()

    return {"message": "Images deleted successfully", "gap_snapshot": db_task.gap_snapshot}


@router.get("/{task_id}/samples")
def get_task_samples(task_id: int, session: SessionDep, token: TokenDep):
    db_task = get_task(task_id, session, token)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db_task.sample
