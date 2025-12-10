from typing import Union

from pydantic import BaseModel, Field


class Rule(BaseModel):

    name: str = Field(..., title="Name", description="The name of the rule.")

    error_message: str = Field(..., title="Error Message", description="The error message associated with the rule.")

    query: str = Field(..., title="Query", description="The query string for the rule.")



class CreateRulesRequest(BaseModel):

    event_type: str = Field(..., title="Event Type",
                            description="The type of event for which the rules are being created.")

    rules: Union[Rule, list[Rule]] = Field(..., title="Rules", description="The rules associated with the event.")


class CreateRulesResponse(BaseModel):

    success: bool = Field(..., title="Success", description="Indicates whether the rules were created successfully.")

    created_rule_ids: list[str] = Field(..., title="Created Rule IDs", description="List of IDs of the created rules.")

    error: str | None = Field(default=None, title="Error", description="Error message if the creation failed.")

    error_code: int | None = Field(default=None, title="Error Code", description="Error code if the creation failed.")


class UpdateRulesRequest(BaseModel):

    event_type: str = Field(..., title="Event Type",
                            description="The type of event for which the rules are being updated.")

    rules: Union[Rule, list[Rule]] = Field(
        ...,
        title="Rules",
        description="The updated rules associated with the event.")
