from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select, or_

from ..schemas.user import User, UserCreate, UserPublic, UserUpdate
from ..utils.functions import get_password_hash
from ..utils.dependencies import SessionDep, TokenDep

router = APIRouter(prefix='/users', tags=["User"])


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, session: SessionDep, token: TokenDep):
    hashed_pwd = get_password_hash(user_create.password)
    db_user = User.model_validate(user_create, update={'password_hash': hashed_pwd})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate, session: SessionDep, token: TokenDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_update.model_dump(exclude_unset=True)

    if 'password' in user_data:
        hashed_pwd = get_password_hash(user_data["password"])
        db_user.sqlmodel_update(user_data, update={"password_hash": hashed_pwd})

    db_user.sqlmodel_update(user_data)

    session.add(db_user)
    session.commit()
    return db_user


@router.get('/search')
def search_users(session: SessionDep, user_id: TokenDep, query: str = ""):

    search_pattern = f"%{query}%"
    conditions = or_(
        User.name.ilike(search_pattern),
        User.role.ilike(search_pattern),  # 不区分大小写的模糊匹配
    )
    stmt = select(
        User.id,
        User.name,
    ).where(conditions)
    results = session.exec(stmt).mappings().all()
    return results


@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: SessionDep, token: TokenDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get('/', response_model=list[UserPublic])
def get_users(session: SessionDep, token: TokenDep):
    users = session.exec(select(User)).all()
    return users


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, token: TokenDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(db_user)
    session.commit()
    return {"message": "User deleted successfully"}
