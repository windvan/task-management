from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
import os


class Settings(BaseSettings):
    # 环境设置,default = development
    ENV: str = 'development'

    # 数据库设置
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME:  str | None = 'database'

    # JWT 设置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_COOKIE_MAX_AGE_SECONDS: int = 604800

    # 前端设置
    FRONT_END_HOST: str = "http://localhost:5173"

    # URLss -- auto
    DATABASE_URL: str | None = None
    BASE_URL: str = os.path.dirname(os.path.abspath(__file__))
    GAP_IMAGE_DIR: str = os.path.abspath(BASE_URL + "statics/images/gaps")

    # middlewares
    CSRF_SECRET: str

    @field_validator("DATABASE_URL")
    def assemble_db_url(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        if info.data.get("ENV") == "production":
            return (
                f"mysql://{info.data.get('DB_USER')}:{info.data.get('DB_PASSWORD')}@"
                f"{info.data.get('DB_HOST')}:{info.data.get('DB_PORT')}/{info.data.get('DB_NAME')}"
            )
        else:
            # 开发环境使用 SQLite
            return f"sqlite:///./{info.data.get('DB_NAME')}.db"

    class Config:

        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建设置实例,根据环境变量ENV,读取不同的配置：dev.env/prod.env
env_file = 'dev.env' if os.getenv('EVN', 'development') == 'development' else 'prod.env'
settings = Settings(_env_file=env_file)


# import os
# from pydantic import BaseModel


# class ConfigBase(BaseModel):
#     # base config
#     BASE_URL: str = os.path.dirname(os.path.abspath(__file__))
#     GAP_IMAGE_DIR: str = os.path.abspath(BASE_URL + "statics/images/gaps")
#     SECRET_KEY: str = "EyAwGbTZ5mhASudyUb4V7rmKH70Qk4Ve"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 30 minutes
#     COOKIE_MAX_AGE_SECONDS: int = 604800  # 7 days, 7*24*3600


# class ConfigDev(ConfigBase):
#     # development config
#     BASE_URL: str = os.path.dirname(os.path.abspath(__file__))
#     DB_URL: str = f"sqlite:///{BASE_URL + os.path.sep}database.db"
#     FRONT_END_HOST: str = "http://localhost:5173"


# class ConfigProd(ConfigBase):
#     # production config
#     DB_URL: str = "mysql+pymysql://"
#     FRONT_END_HOST: str = "https://localhost:5173"


# env: str = os.getenv('ENV', "dev")

# if env == "dev":
#     config = ConfigDev()

# if env == "prod":
#     config = ConfigProd()
