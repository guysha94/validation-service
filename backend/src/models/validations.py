from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class ValidateRequest(BaseModel):

    event_type: str = Field(..., title="Event Type", description="The type of event to validate.")

    url: HttpUrl = Field(..., title="URL", description="The URL to validate the event against.")



class ValidateResponse(BaseModel):
    status: Literal["valid", "invalid"] = Field(..., title="Status", description="The status of the validation.")

    errors:list[str] = Field(default_factory=list,
                             title="Errors",
                             description="List of validation error messages, if any.")
