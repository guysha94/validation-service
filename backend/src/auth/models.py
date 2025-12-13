from typing import Optional, Self

from python_sdk.domain.base import BaseModel
from python_sdk.utils import Crypto
from sqlmodel import Field, SQLModel

from ..users.models import UserShow


class TokenData(BaseModel):
    id: Optional[str] = Field(default=None, title="User ID", description="The user ID.")
    name: Optional[str] = Field(default=None, title="User Name", description="The user's name.")
    email: Optional[str] = Field(default=None, title="Email", description="The user's email.")



class LoginRequest(BaseModel):
    email: str = Field(..., title="Email", description="The email address of the user.")
    password: str = Field(..., title="User Password", description="The user's password.")


class LoginResponse(BaseModel):

    user: UserShow = Field(..., title="User", description="The authenticated user's details.")
    access_token: str = Field(..., title="Access Token", description="The access token string.")
    token_type: str = Field(..., title="Token Type", description="The type of the token.")


class TokenShow(BaseModel):
    access_token: str = Field(..., title="Access Token", description="The access token string.")
    token_type: str = Field(..., title="Token Type", description="The type of the token.")


class TokenCreate(BaseModel):
    access_token: str = Field(..., title="Access Token", description="The access token string.")
    token_type: str = Field(..., title="Token Type", description="The type of the token.")
    user_id: str = Field(..., title="User ID", description="The user's ID.")


class Token(SQLModel, table=True):

    __tablename__ = "tokens"
    id: str = Field(default_factory=Crypto.uuidv7, primary_key=True, title="Token ID",
                    description="The unique identifier for the token.")
    access_token: str = Field(..., title="Access Token", description="The access token string.", index=True)
    token_type: str = Field(..., title="Token Type", description="The type of the token.")
    user_id: str = Field(
        ...,
        title="User ID",
        description="The user's ID.",
        foreign_key="users.id",
        index=True,
    )

    def to_show(self) -> TokenShow:
        return TokenShow(
            access_token=self.access_token,
            token_type=self.token_type
        )

    @classmethod
    def from_create(cls, token_create: TokenCreate) -> Self:
        return cls(
            access_token=token_create.access_token,
            token_type=token_create.token_type,
            user_id=token_create.user_id
        )
