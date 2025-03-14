from fastapi import APIRouter, status, HTTPException
from sqlmodel import select, text, or_, and_

from ..schemas.project import Project, ProjectCreate, ProjectPublic, ProjectUpdate
from ..schemas.product import Product
from ..schemas.task import Task
from ..schemas.user import User
from ..utils.dependencies import SessionDep, TokenDep


router = APIRouter(prefix='/projects', tags=["Project"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(project_create: dict, session: SessionDep, token: TokenDep):

    db_project = Project.model_validate(project_create, from_attributes=True)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    stmt = select(
        Project.__table__.columns,
        Product.internal_name.label("product_internal_name"),
        Product.stage.label("product_stage"),
        User.name.label("portfolio_contact_name")
    ).join(Project.product).join(
        User, Project.portfolio_contact_id == User.id
    ).where(Project.id == db_project.id)

    new_project = session.exec(stmt).mappings().first()
    return new_project


@router.get("/{project_id:int}", response_model=ProjectPublic)
def get_project(project_id: int, session: SessionDep, token: TokenDep):

    stmt = select(
        Project.__table__.columns,
        Product.internal_name.label("product_internal_name"),
        Product.stage.label("product_stage"),
        User.name.label("portfolio_contact_name")
    ).join(Project.product).join(
        User, Project.portfolio_contact_id == User.id
    ).where(Project.id == project_id)

    db_project = session.exec(stmt).mappings().first()
    if not db_project:
        raise HTTPException(status_code=204, detail="project not found")
    return db_project


@router.get("/")
def get_projects(session: SessionDep, user_id: TokenDep):
    query = select(
        Project.__table__.columns,
        Product.internal_name.label("product_internal_name"),
        Product.stage.label("product_stage"),
        User.name.label("portfolio_contact_name")
    ).join(Project.product).join(
        User, Project.portfolio_contact_id == User.id
    )

    db_projects = session.exec(query).mappings().all()
    return db_projects


@router.get('/search')
def search_projects(session: SessionDep, user_id: TokenDep, query: str = ""):
    search_pattern = f"%{query}%"
    conditions = or_(
        Project.project_name.ilike(search_pattern),
        Product.trade_name.ilike(search_pattern),
        Product.internal_name.ilike(search_pattern),  # 不区分大小写的模糊匹配
    )
    stmt = select(
        Project.id,
        Project.project_name,
    ).join(Project.product).where(conditions)

    results = session.exec(stmt).mappings().all()  # 转换为字典格式
    return results


@router.get('/{project_id}/tasks')
def get_related_tasks(project_id: int,  session: SessionDep, token: TokenDep):
    query = select(
        Task.__table__.columns,
        User.name.label("task_owner_name")
    ).join(
        User, User.id == Task.task_owner_id
    ).where(
        Task.project_id == project_id
    )
    db_tasks = session.exec(query).mappings().all()
    return db_tasks


@router.patch('/{project_id}')
def update_project(project_id: int, project_update: ProjectUpdate, session: SessionDep, token: TokenDep):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="project not found")

    project_data = project_update.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    session.add(db_project)
    session.commit()
    stmt = select(
        Project.__table__.columns,
        Product.internal_name.label("product_internal_name"),
        Product.stage.label("product_stage"),
        User.name.label("portfolio_contact_name")
    ).join(Project.product).join(
        User, Project.portfolio_contact_id == User.id
    ).where(Project.id == project_id)

    new_project = session.exec(stmt).mappings().first()
    return new_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep, token: TokenDep):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="project not found")
    session.delete(db_project)
    session.commit()
    return {"message": "project deleted successfully"}
