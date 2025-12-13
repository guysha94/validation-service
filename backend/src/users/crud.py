from sqlmodel import select, update, delete

from .models import User, UserUpdate, UserCreate
from ..db.sqlite_client import get_session


class UserCRUD(object):

    @staticmethod
    async def create(user: UserCreate) -> User:

        db_user = User.from_create(user)
        async with get_session() as session:
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user

    @staticmethod
    async def get_by_id(user_id: str) -> User:
        async with get_session() as session:
            statement = select(User).where(User.id == user_id)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(email: str) -> User:
        async with get_session() as session:
            statement = select(User).where(User.email == email)
            result = await session.execute(statement)
            return result.scalar_one_or_none()


    @staticmethod
    async def get_all() -> list[User]:
        async with get_session() as session:
            statement = select(User)
            result = await session.execute(statement)
            return result.scalars().all()

    @staticmethod
    async def update_one(user_id: str, user: UserUpdate) -> User:
        async with get_session() as session:
            statement = (
                update(User).
                where(User.id == user_id).
                values(**user.model_dump(exclude_unset=True)).
                returning(User)
            )
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_one(user_id: str) -> None:
        async with get_session() as session:
            statement = delete(User).where(User.id == user_id)
            await session.execute(statement)
            await session.commit()
