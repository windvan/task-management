from fastapi import APIRouter, status, HTTPException
from sqlmodel import select, text

from ..schemas.project import Project, ProjectCreate, ProjectPublic, ProjectUpdate
from ..schemas.product import Product
from ..schemas.task import Task
from ..schemas.user import User
from ..utils.dependencies import SessionDep, TokenDep


router = APIRouter(prefix='/projects', tags=["Project"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(project_create: dict, session: SessionDep, token: TokenDep):
    print("get here")
    print("\n\n\n\n@\n", project_create)

    db_project = Project.model_validate(project_create, from_attributes=True)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@router.get("/{project_id:int}", response_model=ProjectPublic)
def get_project(project_id: int, session: SessionDep, token: TokenDep):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="project not found")
    return db_project


@router.get("/")
def get_projects(session: SessionDep, token: TokenDep):
    query = select(
        Project.__table__.columns,
        Product.internal_name.label("product_internal_name"),
        Product.lead_ai.label("product_lead_ai"),
        Product.stage.label("product_stage"),
        User.name.label("portfolio_contact_name")
    ).join(
        Product, Project.product_id == Product.id
    ).join(
        User, Project.portfolio_contact_id == User.id
    )

    db_projects = session.exec(query).mappings().all()
    return db_projects



@router.get('/{project_id}/tasks')
def get_related_tasks(project_id: int,  session: SessionDep, token: TokenDep):
    query=select(
        Task.__table__.columns,        
        User.name.label("task_owner_name")
    ).join(
        User,User.id==Task.task_owner_id
    ).where(
        Task.project_id == project_id
        )
    db_tasks = session.exec(query).mappings().all()
    if not db_tasks:
        raise HTTPException(status_code=404, detail="No related tasks")
    return db_tasks


@router.get('/select-options')
def get_select_options(session: SessionDep, token: TokenDep):

    product_list = session.exec(select(Product.id, Product.internal_name)).mappings().all()
    user_list = session.exec(select(User.id, User.name)).mappings().all()

    return {
        "productOptions": product_list,
        "userOptions": user_list
    }


@router.patch('/{project_id}')
def update_project(project_id: int, project_update: ProjectUpdate, session: SessionDep, token: TokenDep):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="project not found")

    project_data = project_update.model_dump(exclude_unset=True)
    db_project.sqlmodel_update(project_data)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep, token: TokenDep):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="project not found")
    session.delete(db_project)
    session.commit()
    return {"message": "project deleted successfully"}
