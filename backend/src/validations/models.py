from datetime import datetime, UTC
from typing import Literal, Self, Optional

from pydantic import HttpUrl
from python_sdk.domain.base import BaseModel
from python_sdk.utils import Crypto
from sqlmodel import Field, SQLModel


class ValidationCreate(BaseModel):

    event_type: str = Field(..., title="Event Type", description="The type of event to validate.")
    label: Optional[str] = Field(default=None, title="Label", description="An optional label for the validation.")
    icon: Optional[str] = Field(default=None, title="Icon", description="An optional icon for the validation.")

class ValidationUpdate(BaseModel):

    event_type: Optional[str] = Field(default=None, title="Event Type", description="The type of event to validate.")
    label: Optional[str] = Field(default=None, title="Label", description="An optional label for the validation.")
    icon: Optional[str] = Field(default=None, title="Icon", description="An optional icon for the validation.")

class Validation(SQLModel, table=True):

    __tablename__ = "validations"

    id: str = Field(
        default_factory=Crypto.uuidv7,
        primary_key=True, title="Validation ID",
        description="The unique identifier for the validation."
    )

    event_type: str = Field(..., title="Event Type", description="The type of event to validate.")
    label: Optional[str] = Field(default=None, title="Label", description="An optional label for the validation.")
    icon: Optional[str] = Field(default=None, title="Icon", description="An optional icon for the validation.")

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        title="Updated At",
        description="The timestamp when the validation was last updated."
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        title="Created At",
        description="The timestamp when the validation was created."
    )

    @classmethod
    def from_create(cls, create: ValidationCreate) -> Self:
        return cls(event_type=create.event_type)


class ValidateRequest(BaseModel):

    event_type: str = Field(..., title="Event Type", description="The type of event to validate.")

    url: HttpUrl = Field(..., title="URL", description="The URL to validate the event against.")


class ValidateResponse(BaseModel):
    status: Literal["valid", "invalid"] = Field(..., title="Status", description="The status of the validation.")

    errors: list[str] = Field(default_factory=list,
                              title="Errors",
                              description="List of validation error messages, if any.")
