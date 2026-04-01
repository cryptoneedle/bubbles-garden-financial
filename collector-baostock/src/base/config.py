from functools import cache
from typing import Any
from urllib.parse import quote_plus

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """数据库连接配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="DB_",  # 开启全局前缀，省去大批 alias
    )

    # 1. 基础配置：极简写法（根据 env_prefix 自动匹配 DB_HOST 等）
    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: SecretStr

    # 仍需 alias 的特例（如果不想改变环境变量命名）
    name: str = Field(alias="DB_NAME")
    schema_name: str = Field(default="public", alias="DB_SCHEMA")

    # 2. 带有校验的连接池配置
    pool_size: int = Field(default=5, ge=1, le=20)
    max_overflow: int = Field(default=10, ge=0)
    pool_timeout: int = Field(default=30, ge=1)
    pool_recycle: int = Field(default=3600, ge=60)
    echo: bool = False
    pool_pre_ping: bool = True

    @model_validator(mode="after")
    def validate_pool_config(self) -> "DatabaseSettings":
        """校验连接池安全性"""
        if self.pool_size + self.max_overflow > 100:
            raise ValueError("pool_size + max_overflow 不应超过 100")
        return self

    def get_url(self, is_async: bool = False) -> str:
        """获取并构建数据库连接 URL"""
        driver = "asyncpg" if is_async else "psycopg2"
        pwd = quote_plus(self.password.get_secret_value())
        return f"postgresql+{driver}://{self.username}:{pwd}@{self.host}:{self.port}/{self.name}"

    def get_engine_options(self, is_async: bool = False) -> dict[str, Any]:
        """获取 SQLAlchemy Engine 完整配置"""
        # 一次性提取所有池配置
        options = self.model_dump(
            include={"pool_size", "max_overflow", "pool_timeout", "pool_recycle", "pool_pre_ping", "echo"}
        )

        # 精简的三元操作拼接
        options["connect_args"] = (
            {"server_settings": {"search_path": self.schema_name}} if is_async
            else {"options": f"-c search_path={self.schema_name}"}
        )
        return options

    def get_safe_info(self) -> dict[str, Any]:
        """获取脱敏配置，用于日志/健康检查"""
        return self.model_dump(exclude={"password"})


@cache
def get_db_settings() -> DatabaseSettings:
    """获取数据库配置单例（进程内缓存）"""
    return DatabaseSettings()

@cache
def get_schema() -> DatabaseSettings:
    """获取数据库配置单例（进程内缓存）"""
    return DatabaseSettings().schema_name