from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from sqlalchemy import or_

from app.schemas.product import Product
from app.schemas.project import Project
from app.schemas.user import User

from ..schemas.sample import Sample, SampleCreate, SamplePublic, SampleUpdate
from ..schemas.task import Task

from ..utils.dependencies import SessionDep, TokenDep

router = APIRouter(prefix='/samples', tags=["Sample"])


@router.post("/", response_model=SamplePublic | list[SamplePublic], status_code=status.HTTP_201_CREATED)
def create_sample(sample_create: SampleCreate, session: SessionDep):
    if isinstance(sample_create, list):
        # 处理多条记录
        db_samples = []
        for sample in sample_create:
            db_sample = Sample.model_validate(sample)
            session.add(db_sample)
            db_samples.append(db_sample)
        session.commit()
        for db_sample in db_samples:
            session.refresh(db_sample)
        return db_samples
    else:
        # 处理单条记录
        db_sample = Sample.model_validate(sample_create)
        session.add(db_sample)
        session.commit()
        session.refresh(db_sample)
        return db_sample


@router.get('/')
def get_samples(session: SessionDep):
    stmt = select(*(Sample.__table__.columns), Product.internal_name.label("product_internal_name")).join(Sample.product)
    db_samples = session.exec(stmt).mappings().all()

    return db_samples


@router.get('/search')
def search_projects(session: SessionDep, query: str = ""):
    search_pattern = f"%{query}%"
    conditions = or_(
        Project.project_name.ilike(search_pattern),
        Product.trade_name.ilike(search_pattern),
        Product.internal_name.ilike(search_pattern),  # 不区分大小写的模糊匹配
    )
    stmt = select(
        Sample.id,
        Sample.sample_name,
    ).join(Sample.product).where(conditions)

    results = session.exec(stmt).mappings().all()  # 转换为字典格式
    return results



@router.delete('/{sample_id}')
def delete_sample(sample_id: int, session: SessionDep):
    db_sample = session.get(Sample, sample_id)
    if not db_sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    session.delete(db_sample)
    session.commit()
    return db_sample


@router.get('/{sample_id}/tasks')
def get_sample_tasks(sample_id: int, session: SessionDep):
    stmt = (select(Sample.id.label('sample_id'),
                   Task.id,
                   Task.task_name,
                   Task.task_status,
                   Task.task_progress,
                   User.name.label('task_owner'),
                   Project.project_name).join(Sample.tasks).where(Sample.id == sample_id).join(Task.task_owner).join(Task.project).order_by(Task.task_status))
    sample_tasks = session.exec(stmt).mappings().all()

    return sample_tasks


@router.post('/{sample_id}/tasks')
def relate_sample_task(sample_id: int, task_id_list: list[int], session: SessionDep):
    db_sample = session.get(Sample, sample_id)
    if not db_sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    if not task_id_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task list is empty")
    for task_id in task_id_list:
        db_task = session.get(Task, task_id)
        db_sample.tasks.append(db_task)
    session.commit()

    return db_sample.tasks


@router.delete('/{sample_id}/tasks/{task_id}')
def delete_sample_task(sample_id: int, task_id: int, session: SessionDep):
    db_sample = session.get(Sample, sample_id)
    if not db_sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db_sample.tasks.remove(db_task)
    session.commit()
    return db_sample.tasks


@router.patch('/{sample_id}', response_model=SamplePublic)
def update_sample(sample_id: int, sample_update: SampleUpdate, session: SessionDep):
    db_sample = session.get(Sample, sample_id)
    if not db_sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")
    db_sample.sqlmodel_update(sample_update.model_dump(exclude_unset=True))

    session.add(db_sample)
    session.commit()
    session.refresh(db_sample)
    return db_sample


