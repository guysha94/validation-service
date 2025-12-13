from typing import Literal

from pydantic import HttpUrl
from python_sdk.domain.base import BaseModel
from python_sdk.utils import Crypto
from sqlmodel import Field, SQLModel


class Validation(SQLModel, table=True):

    __tablename__ = "validations"

    id: str = Field(
        default_factory=Crypto.uuidv7,
        primary_key=True, title="Validation ID",
        description="The unique identifier for the validation."
    )

    event_type: str = Field(..., title="Event Type", description="The type of event to validate.")



class ValidateRequest(BaseModel):

    event_type: str = Field(..., title="Event Type", description="The type of event to validate.")

    url: HttpUrl = Field(..., title="URL", description="The URL to validate the event against.")



class ValidateResponse(BaseModel):
    status: Literal["valid", "invalid"] = Field(..., title="Status", description="The status of the validation.")

    errors:list[str] = Field(default_factory=list,
                             title="Errors",
                             description="List of validation error messages, if any.")
