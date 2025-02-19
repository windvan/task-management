# cookie token authentication
from fastapi import APIRouter,  HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from sqlmodel import select,  SQLModel
import jwt
from datetime import datetime, timedelta, timezone

from ..schemas.user import User
from ..utils.functions import verify_password
from ..utils.dependencies import SessionDep, TokenDep, CurrentUserDep
from ..config import settings

router = APIRouter(prefix='/auth', tags=["JwtAuth"])


def create_token(user: User, scopes: list):
    access_token_expires: datetime = datetime.now(tz=timezone(
        timedelta(hours=8))) + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
    # iss(issuer): 令牌的发行者
    # sub(subject): 令牌的主题
    # aud(audience): 令牌的接收者
    # exp(expiration time): 过期时间
    # nbf(not before): 在此之前不可用
    # iat(issued at): 发行时间
    # jti(JWT ID): 令牌的唯一标识符
    payload = {"sub": user.id, "exp": access_token_expires, "scopes": scopes}
    encoded_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt


class Credential(SQLModel):
    username: EmailStr  # email
    password: str


@router.post('/login')
def password_login(session: SessionDep, credential: Credential):

    user: User = session.exec(select(User).where(
        User.email == credential.username.lower())).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username does not exist!",
        )

    if not verify_password(credential.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password!",
        )

    access_token = create_token(user, ["all"])

    response = JSONResponse(content={
        "current_user": user.model_dump(include=['id', 'name', 'email', 'role']),
        "isAuthenticated": True
    })

    response.set_cookie(
        path="/",
        key="access_token",
        value=access_token,
        max_age=settings.JWT_COOKIE_MAX_AGE_SECONDS,
        httponly=True,
        secure=True,  # https required
        samesite="none"
    )
    return response


@router.post('/refresh')
# use current valid token to get a new token.
# auto requst from frontend
async def refresh_token(user_id: TokenDep):
    payload = jwt.decode(access_token, key=settings.JWT_SECRET_KEY,
                         algorithms=settings.JWT_ALGORITHM)
    payload['exp'] = datetime.now(tz=timezone(timedelta(hours=8))) + \
        timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)

    access_token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

    response = JSONResponse()

    response.set_cookie(
        path="/",
        key="access_token",
        value=access_token,
        max_age=settings.JWT_COOKIE_MAX_AGE_SECONDS,
        httponly=True,
        secure=True,  # https required
        samesite="none"
    )
    return response


@router.get('/logout')
def log_out(user_id: TokenDep):
    response = JSONResponse(content={'detail': 'logged out successfully!'},
                            status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key='access_token',
                           samesite="none",
                           secure=True
                           )
    return response


@router.get("/auth/status")
async def get_auth_status(current_user: CurrentUserDep):
    return {
        "isAuthenticated": True,
        "current_user": current_user.model_dump(include=['id', 'name', 'email', 'role'])
    }


@router.post('/sso')
def SSO_callback():
    return {"message": "SSO Callback success!"}
