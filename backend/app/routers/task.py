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


@router.get('/select-options')
def get_select_options(session: SessionDep, token: TokenDep):

    project_list = session.exec(
        select(Project.id, Project.project_name)).mappings().all()
    user_list = session.exec(select(User.id, User.name)).mappings().all()
    cro_list = session.exec(select(Cro.id, Cro.cro_name)).mappings().all()
    sample_list = session.exec(
        select(Sample.id, Sample.sample_name)).mappings().all()

    task_library = session.exec(select(TaskLibrary)).all()

    tree = []
    for task in task_library:
        node = [item for item in tree if item.get(
            'label') == task.task_category]

        if node:
            node[0]["children"].append(
                {'key': task.id, 'label': task.task_name_prefix, 'data': task.task_name_prefix})
        else:
            tree.append({'key': task.task_category, 'label': task.task_category,
                         'data': task.task_category, 'children': [{'key': task.id, 'label': task.task_name_prefix, 'data': task.task_name_prefix}]})

    return {
        "projectOptions": project_list,
        "userOptions": user_list,
        "croOptions": cro_list,
        "sampleOptions": sample_list,
        "taskLibrary": task_library,
        "taskTree": tree
    }


@router.get('/search')
def search_tasks(session: SessionDep, user_id: TokenDep, query: str = "",sample_id=None):
    search_pattern = f"%{query}%"
    conditions = and_(
        or_(
            Product.trade_name.ilike(search_pattern),
            Product.internal_name.ilike(search_pattern),
            Task.task_name.ilike(search_pattern),  # 不区分大小写的模糊匹配
            Task.tags.ilike(search_pattern)),
        User.id == user_id,
        ~Task.samples.any(Sample.id == sample_id) if sample_id else True
    )
    stmt = select(
        Task.id,
        Task.task_name,
        Task.tags,
        Product.internal_name.label("product_internal_name"),
        Product.trade_name.label("product_trade_name"),

    ).join(Task.project).join(Project.product).join(Task.task_owner).where(conditions)

    results = session.exec(stmt).mappings().all()
    # 转换为字典格式
    return results


@router.get("/{task_id}", response_model=TaskPublic)
def get_task(task_id: int, session: SessionDep, token: TokenDep):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")
    return db_task


class TaskSamples(SQLModel):
    # id: int
    # sample_name: str
    sample_status: SampleStatusEnum


class TaskWithSample(TaskPublic):
    # project_name: str
    # cro_name: str
    samples: list[TaskSamples]


@router.get("/")
def get_tasks(session: SessionDep, token: TokenDep):

    db_tasks = session.exec(select(Task)).all()

    return [{
        **task.model_dump(exclude={"project_id", "task_owner_id", "cro_id", "gap_id"}),
        "project_name": task.project.project_name if task.project else None,
        "task_owner_name": task.task_owner.name if task.task_owner else None,
        "cro_name": task.cro.cro_name if task.cro else None,
        "gap_snapshot_url": task.gap.snapshot_url if task.gap else None,
        "samples": [
            {"id": s.id, "status": s.sample_status}
            for s in task.samples
        ]
    } for task in db_tasks]


# one or more tasks to patch
@router.patch('/', response_model=list[TaskPublic])
def update_task(tasks_to_update: dict[int, dict], session: SessionDep, token: TokenDep):

    updated_tasks = []
    for task_id, task_data in tasks_to_update.items():
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail=f"Task with id {
                                task_id} not found")

        # task_update = task_data.model_dump(exclude_unset=True)
        db_task.sqlmodel_update(task_data)
        session.add(db_task)
        updated_tasks.append(db_task)

    session.commit()
    # refresh all updated tasks
    for task in updated_tasks:
        session.refresh(task)

    return updated_tasks


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

    print("\n\n\n\n", db_task.gap_snapshot)
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

    return db_task.samples
