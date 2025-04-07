from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, ValidationInfo
import os
from pathlib import Path


class Settings(BaseSettings):

    ENV: str

    # 数据库设置
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME:  str | None = 'test_db'

    # 静态文件设置
    STATIC_ROOT: str
    STATIC_GAP_FOLDER: str

    # JWT 设置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_COOKIE_MAX_AGE_SECONDS: int = 604800

    # 前端设置
    FRONT_END_HOST: str = "http://localhost:5173"

    # URLss -- auto
    DATABASE_URL: str | None = None
    BASE_URL: Path = Path(__file__).parent
    GAP_IMAGE_DIR: Path = BASE_URL / "statics/images/gaps"

    # middlewares
    # CSRF_SECRET: str

    @field_validator("DATABASE_URL")
    def assemble_db_url(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        if info.data.get("ENV") == "production":
            # 生产环境使用 MySQL
            return (
                f"mysql+pymysql://{info.data.get('DB_USER')}:{info.data.get('DB_PASSWORD')}@"
                f"{info.data.get('DB_HOST')}:{info.data.get('DB_PORT')}/{info.data.get('DB_NAME')}"
            )
        else:
            # 开发环境使用 SQLite
            # return "sqlite:///" + Path(__file__).parent.joinpath(f"{info.data.get('DB_NAME')}.db").resolve().as_posix()
            return f"sqlite:///./app/database/{info.data.get('DB_NAME')}.db" 
            

    # config env file
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / 'env.env', env_file_encoding='utf-8', case_sensitive=True)


# 创建Settings实例,根据环境变量ENV,读取不同的配置：dev.env/prod.env
settings = Settings()
