import logging
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import Field, MySQLDsn, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from python_sdk.conf.app_settings import BooleanField, PathField, base_model_config
from python_sdk.conf.app_settings import Settings as _Settings


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        **base_model_config,
        env_prefix="auth_",
        cli_prefix="auth_",
    )

    secret: SecretStr = Field(
        default="supersecretkey",
        title="The secret key",
        description="The secret key for signing tokens",
    )

    algorithm: str = Field(default="HS256", title="The algorithm", description="The algorithm")

    expires_in_minutes: PositiveInt = Field(
        default=30,
        title="The token expiration time in minutes",
        description="The token expiration time in minutes",
    )


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        **base_model_config,
        env_prefix="api_",
        cli_prefix="api_",
    )
    host: str = Field(
        default="0.0.0.0",
        title="The host address",
        description="The host address",
    )
    port: int = Field(
        default=3000,
        title="The port number",
        description="The port number",
    )


class MySQLSettings(BaseSettings):
    model_config = SettingsConfigDict(
        **base_model_config,
        env_prefix="mysql_",
        cli_prefix="mysql_",
    )
    url: str = Field(
        default="mysql+asyncmy://root:masterkey@127.0.0.1:3306/backend",
        title="The MySQL connection URL",
        description="The MySQL connection URL",
    )

    pool_size: PositiveInt = Field(default=100, title="The pool size", description="The pool size")
    max_overflow: PositiveInt = Field(default=20, title="The max overflow", description="The max overflow")
    connect_timeout: PositiveInt = Field(default=10, title="The connection timeout",
                                         description="The connection timeout in seconds")
    isolation_level: str = Field(default="READ COMMITTED", title="The isolation level",
                                 description="The isolation level")

    @property
    def dsn(self) -> MySQLDsn:
        return MySQLDsn(self.url.replace("mysql://", "mysql+asyncmy://"))


class SqliteSettings(BaseSettings):
    model_config = SettingsConfigDict(
        **base_model_config,
        env_prefix="sqlite_",
        cli_prefix="sqlite_",
    )
    path: PathField = Field(
        default_factory=lambda: Path("./db.sqlite3"),
        title="The Sqlite database file path",
        description="The Sqlite database file path",
    )


    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.path}"


class Settings(_Settings):
    model_config = SettingsConfigDict(**base_model_config)
    env: str = Field(
        default="dev", title="The environment", description="The environment"
    )

    base_dir: PathField = Field(
        default_factory=Path.cwd, description="The base directory"
    )

    debug: BooleanField = Field(default=False, description="Debug mode")

    timezone_name: str = Field(
        default="Asia/Jerusalem",
        description="The app timezone",
        alias="timezone",
    )

    api: APISettings = APISettings()
    mysql: MySQLSettings = MySQLSettings()
    sqlite: SqliteSettings = SqliteSettings()
    auth: AuthSettings = AuthSettings()

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone_name)

    @property
    def is_dev(self) -> bool:
        return "dev" in self.env.lower()

    @property
    def is_prod(self) -> bool:
        return "prod" in self.env.lower()

    @property
    def is_test(self) -> bool:
        return "test" in self.env.lower()

    @property
    def is_staging(self) -> bool:
        return "staging" in self.env.lower()

    @property
    def static_dir(self) -> Path:
        return self.base_dir / "static"

    @property
    def log_level(self) -> int:
        return logging.DEBUG if self.is_dev or self.debug else logging.INFO


settings: Settings = Settings()  # noqa
