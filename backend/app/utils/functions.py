from datetime import datetime, timezone, date
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta



# 创建一个 CryptContext 实例，指定使用 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_bj_now() -> datetime:
    # get current time of Beijng timezone
    return datetime.now(tz=timezone(timedelta(hours=8)))


