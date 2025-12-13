from typing import Optional, Self

from python_sdk.domain.base import BaseModel
from python_sdk.utils import Crypto
from sqlmodel import Field, SQLModel


class UserCreate(BaseModel):
    name: Optional[str] = Field(default_factory=str, title="User Name", description="The user's name.")
    email: str = Field(..., title="Email", description="The email address of the user.")
    password: str = Field(..., title="User Password", description="The user's password.")


class UserShow(BaseModel):
    id: str = Field(..., title="User ID", description="The unique identifier for the user.")
    name: str = Field(..., title="User Name", description="The user's name.")
    email: str = Field(..., title="Email", description="The email address of the user.")
    disabled: bool = Field(..., title="Disabled", description="Indicates whether the user is disabled.")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, title="User Name", description="The user's name.")
    email: Optional[str] = Field(default=None, title="Email", description="The email address of the user.")
    password: Optional[str] = Field(default=None, title="User Password", description="The user's password.")
    disabled: Optional[bool] = Field(default=None, title="Disabled", description="Indicates whether the user is disabled.")




class User(SQLModel, table=True):

    __tablename__ = "users"
    id: str = Field(
        default_factory=Crypto.uuidv7,
        primary_key=True,
        title="User ID",
        description="The unique identifier for the user.")

    name: str = Field(default_factory=str, title="User Name", description="The user's name.")

    email: str = Field(..., title="Email", description="The email address of the user.", index=True)

    password: str = Field(..., title="User Password", description="The user's password.")

    disabled: bool = Field(default=False, title="Disabled", description="Indicates whether the user is disabled.")

    def to_show(self) -> UserShow:
        return UserShow(
            id=self.id,
            name=self.name,
            email=self.email,
            disabled=self.disabled
        )

    @classmethod
    def from_create(cls, user_create: UserCreate) -> Self:
        return cls(
            name=user_create.name,
            email=user_create.email,
            password=user_create.password
        )
