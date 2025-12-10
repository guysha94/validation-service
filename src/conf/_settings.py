import logging
from pathlib import Path
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import (
    BeforeValidator,
    Field,
)
from pydantic_settings import SettingsConfigDict
from python_sdk.conf.app_settings import Settings as _Settings

PathField = Annotated[Path, BeforeValidator(lambda x: Path(x))]

BooleanField = Annotated[
    bool, BeforeValidator(lambda x: str(x) == "1" or str(x).lower() == "true")
]
base_model_config = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
    "extra": "ignore",
    "validate_assignment": True,
    "case_sensitive": False,
}


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
