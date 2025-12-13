from typing import Optional

from sqlmodel import select, delete

from .models import TokenCreate, Token
from ..db.sqlite_client import get_session


class TokenCRUD(object):

    @staticmethod
    async def create(token: TokenCreate) -> Token:

        db_token = Token.from_create(token)
        async with get_session() as session:
            session.add(db_token)
            await session.commit()
            await session.refresh(db_token)
            return db_token

    @staticmethod
    async def get_by_user_id(user_id: str) -> Optional[Token]:
        async with get_session() as session:
            statement = select(Token).where(Token.user_id == user_id)
            result = await session.execute(statement)
            return result.scalar_one_or_none()


    @staticmethod
    async def get_all() -> list[Token]:
        async with get_session() as session:
            statement = select(Token)
            result = await session.execute(statement)
            return result.scalars().all()


    @staticmethod
    async def delete_by_user_id(user_id: str) -> None:
        async with get_session() as session:
            statement = delete(Token).where(Token.user_id == user_id)
            await session.execute(statement)
            await session.commit()

    @staticmethod
    async def delete_one(token_id: str) -> None:
        async with get_session() as session:
            statement = delete(Token).where(Token.id == token_id)
            await session.execute(statement)
            await session.commit()
