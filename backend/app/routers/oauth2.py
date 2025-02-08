from fastapi import APIRouter,  Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import select, Session
import jwt
from datetime import datetime, timedelta, timezone

from ..schemas import User
from ..utils.functions import verify_password
from ..utils.dependencies import SessionDep, CurrentUserDep, TokenDep
from ..config import config

router = APIRouter(prefix='/auth', tags=["Auth"])


# generate an access_token, stored to secured cookie
# returen token and user
def create_token_response(user: User):

    def create_token(data: dict, exp: datetime):
        to_encode = data.copy()
        to_encode.update({"exp": exp})
        encoded_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, config.ALGORITHM)
        return encoded_jwt

    now = datetime.now()
    access_token_expires: datetime = now + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    cookie_expires: datetime = now + timedelta(seconds=config.COOKIE_MAX_AGE_SECONDS)

    access_token = create_token(data={"sub": user.id}, exp=access_token_expires)

    response = JSONResponse({
        "access_token": access_token,
        "token_type": "Bearer",
        "current_user": user.model_dump(exclude=['password', 'external_id', 'external_auth'])
    })

    response.set_cookie(
        path="/",
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=config.COOKIE_MAX_AGE_SECONDS,
        expires=cookie_expires.astimezone(timezone.utc),
        httponly=True,
        secure=True,  # https required
        samesite="none"
    )

    return response


@router.post('/login')
def access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):

    def authenticate_user(username: str, password: str, session: Session):

        user: User = session.exec(select(User).where(
            User.email == username.lower())).first()
        if not user:
            return False

        if not verify_password(password, user.password_hash):
            return False

        return user

    user: User = authenticate_user(
        form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_token_response(user)


@router.post('/refresh')
# use current valid token to get a new token.
# auto requst from frontend
def refresh_token(session: SessionDep, current_user: CurrentUserDep):
    return create_token_response(current_user)


@router.get('/logout')
def log_out(token: TokenDep):
    response = JSONResponse(content={'message':'logged out successfully!'}, status_code=200)
    response.delete_cookie(key='access_token',
                           samesite="none",
                           secure=True
                           )

    return response


@router.post('/sso')
def SSO_callback():
    return {"message": "SSO Callback success!"}
