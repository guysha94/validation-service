from datetime import UTC, datetime
from typing import Optional, Self, Union

from python_sdk.domain.base import BaseModel
from python_sdk.utils.crypto import uuidv7
from sqlmodel import Field, SQLModel


class RuleCreate(BaseModel):

    validation_id: str = Field(
        ...,
        title="Validation ID",
        description="The ID of the associated validation.",
    )

    name: str = Field(..., title="Name", description="The name of the rule.")

    error_message: str = Field(..., title="Error Message", description="The error message associated with the rule.")

    query: str = Field(..., title="Query", description="The query string for the rule.")


class RuleUpdate(BaseModel):
    name: Optional[str] = Field(default=None, title="Name", description="The name of the rule.")

    error_message: Optional[str] = Field(default=None, title="Error Message",
                                         description="The error message associated with the rule.")

    query: Optional[str] = Field(default=None, title="Query", description="The query string for the rule.")


class RuleUpdateMany(BaseModel):

    id: str = Field(..., title="ID", description="The ID of the rule.")
    changes: RuleUpdate = Field(..., title="Changes", description="The changes to be applied to the rule.")


class Rule(SQLModel, table=True):

    __tablename__ = "rules"

    id: str = Field(default_factory=uuidv7, primary_key=True, title="Token ID",
                    description="The unique identifier for the token.")

    validation_id: str = Field(
        ...,
        title="Validation ID",
        description="The ID of the associated validation.",
        foreign_key="validations.id",
        index=True,
    )

    name: str = Field(..., title="Name", description="The name of the rule.")

    error_message: str = Field(..., title="Error Message", description="The error message associated with the rule.")

    query: str = Field(..., title="Query", description="The query string for the rule.")

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
    def from_create(cls, create: RuleCreate) -> Self:
        return cls(
            validation_id=create.validation_id,
            name=create.name,
            error_message=create.error_message,
            query=create.query
        )


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
