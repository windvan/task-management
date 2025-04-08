from sqlmodel import Session
from fastapi import Depends, HTTPException, status,  Cookie
from collections.abc import Generator
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Annotated

from ..database.db import engine, UserAwareSession
from ..schemas import User
from ..config import settings

# region Token Dependency


async def validate_token(access_token: str = Cookie(default=None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token."
    )

    try:
        payload = jwt.decode(access_token, key=settings.JWT_SECRET_KEY,
                             algorithms=settings.JWT_ALGORITHM)
        # in line with token creation
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    # for validate token,return user_id
    return user_id

TokenDep = Annotated[int, Depends(validate_token)]

# endregion Token Dependency

# region Session dependency

def get_session_with_user(user_id: TokenDep) -> Generator[UserAwareSession, None, None]:
    with UserAwareSession(engine) as session:
        session.set_user_id(user_id)
        yield session


SessionDep = Annotated[Session, Depends(get_session_with_user)]

# endregion Session dependency


async def get_current_user(session: SessionDep):

    user = session.get(User, session._current_user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )
    return user

# for validate token, and get user from db
CurrentUserDep = Annotated[User, Depends(get_current_user)]


