from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from ..conf import settings
from ..users.crud import UserCRUD


class AuthService(object):

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def __init__(self) -> None:
        self.password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    async def authenticate_user(self, email: str, password: str):
        user = await UserCRUD.get_by_email(email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth.expires_in_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.auth.secret.get_secret_value(), algorithm=settings.auth.algorithm)
        return encoded_jwt

    @staticmethod
    def decode_jwt(token: str) -> dict:
        decoded_token = jwt.decode(token, settings.auth.secret.get_secret_value(), algorithms=[settings.auth.algorithm])
        return decoded_token if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp() else None

    @staticmethod
    def is_token_valid(token: str) -> bool:
        decoded_token = jwt.decode(token, settings.auth.secret.get_secret_value(), algorithms=[settings.auth.algorithm])
        return decoded_token["exp"] >= datetime.now(timezone.utc).timestamp()


AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
