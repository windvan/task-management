from datetime import datetime, timezone
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse
# 创建一个 CryptContext 实例，指定使用 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_bj_now() -> datetime:
    # get current time of Beijng timezone
    return datetime.now(tz=timezone(timedelta(hours=8)))

# get schemas of a pydantic model


def get_model_schema(model_name: str):

    model = globals().get(model_name)

    if not model:
        return None

    return model.schema()


# convert javascript date string to utc datetime with timezone
# Tue Mar 25 2025 14:00:37 GMT+0800===2025-03-25 22:00:37+00:00
def date_to_utc(date_string):
    # 解析 JavaScript 日期字符串
    parsed_date = parse(date_string)

    # 如果解析后的日期没有时区信息，假定它是本地时间，并添加时区信息
    if parsed_date.tzinfo is None:
        # parsed_date = parsed_date.replace(tzinfo=datetime.now(timezone.utc).astimezone().tzinfo)
        parsed_date = parsed_date.replace(tzinfo=timezone.utc)

    # 转换为 UTC
    utc_date = parsed_date.astimezone(timezone.utc)

    return utc_date
