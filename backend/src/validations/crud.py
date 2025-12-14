from typing import Optional

from fastapi import HTTPException
from sqlmodel import select, delete

from .models import Validation, ValidationCreate, ValidationUpdate
from ..db.sqlite_client import get_session


class ValidationCRUD(object):

    @staticmethod
    async def create(validation: ValidationCreate) -> Validation:
        db_validation = Validation.from_create(validation)
        async with get_session() as session:
            session.add(db_validation)
            await session.commit()
            await session.refresh(db_validation)
            return db_validation

    @staticmethod
    async def get_by_id(validation_id: str) -> Optional[Validation]:
        async with get_session() as session:
            return await session.get_one(Validation, validation_id)

    @staticmethod
    async def get_all() -> list[Validation]:
        async with get_session() as session:
            res = await session.exec(select(Validation))
            return res.all()

    @staticmethod
    async def delete_one(validation_id: str) -> None:
        async with get_session() as session:
            statement = delete(Validation).where(Validation.id == validation_id)
            await session.execute(statement)
            await session.commit()

    @staticmethod
    async def update_one(validation_id: str, validation: ValidationUpdate) -> Optional[Validation]:
        async with get_session() as session:
            db_validation = await session.get(Validation, validation_id)
            if not db_validation:
                raise HTTPException(status_code=404, detail="Hero not found")
            data = validation.model_dump(exclude_unset=True)
            db_validation.sqlmodel_update(data)
            session.add(db_validation)
            await session.commit()
            await session.refresh(db_validation)
            return db_validation
