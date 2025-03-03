from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from app.schemas.product import Product
from app.schemas.project import Project
from app.schemas.user import User

from ..schemas.sample import Sample, SampleCreate, SamplePublic
from ..schemas.task import Task

from ..utils.dependencies import SessionDep, TokenDep

router = APIRouter(prefix='/samples', tags=["Sample"])


@router.post("/", response_model=SamplePublic | list[SamplePublic], status_code=status.HTTP_201_CREATED)
def create_sample(sample_create: SampleCreate | list[SampleCreate], session: SessionDep, token: TokenDep):
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
def get_samples(session: SessionDep, token: TokenDep):
    stmt = select(Sample,Product.id,Product.internal_name).join(Sample.product)
    db_samples = session.exec(stmt).mappings().all()
    return [{
        **sample.Sample.model_dump(exclude={'product_id'}),
        "product": {
            "id": sample.id,
            "internal_name": sample.internal_name
        }
    } for sample in db_samples]

    # return [{**sample.model_dump(exclude={'product_id'}),
    #          "product_name": sample.product.product_name} for sample in db_samples]


@router.get('/{sample_id}/tasks')
def get_sample_tasks(sample_id: int, session: SessionDep, token: TokenDep):
    stmt = (select(Sample.id.label('sample_id'),
                   Task.task_name,
                   Task.task_status,
                   Task.task_progress,
                   User.name.label('task_owner'),
                   Project.project_name).join(Sample.tasks).where(Sample.id == sample_id).join(Task.task_owner).join(Task.project).order_by(Task.task_status))
    sample_tasks = session.exec(stmt).mappings().all()

    return sample_tasks
