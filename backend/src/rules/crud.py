from typing import Optional

from fastapi import HTTPException
from sqlmodel import delete, select

from ..db.sqlite_client import get_session
from .models import Rule, RuleCreate, RuleUpdate, RuleUpdateMany


class RulesCRUD(object):

    @staticmethod
    async def create(rule: RuleCreate) -> Rule:
        db_rule = Rule.from_create(rule)
        async with get_session() as session:
            session.add(db_rule)
            await session.commit()
            await session.refresh(db_rule)
            return db_rule

    @staticmethod
    async def create_many(rules: list[RuleCreate]) -> list[Rule]:
        db_rules = [Rule.from_create(rule) for rule in rules]
        async with get_session() as session:
            session.add_all(db_rules)
            await session.commit()
            for db_rule in db_rules:
                await session.refresh(db_rule)
            return db_rules

    @staticmethod
    async def get_by_id(rule_id: str) -> Optional[Rule]:
        async with get_session() as session:
            return await session.get_one(Rule, rule_id)

    @staticmethod
    async def get_all() -> list[Rule]:
        async with get_session() as session:
            res = await session.exec(select(Rule))
            return res.all()

    @staticmethod
    async def delete_one(rule_id: str) -> None:
        async with get_session() as session:
            statement = delete(Rule).where(Rule.id == rule_id)
            await session.execute(statement)
            await session.commit()

    @staticmethod
    async def update_one(rule_id: str, rule: RuleUpdate) -> Optional[Rule]:
        async with get_session() as session:
            db_validation = await session.get(Rule, rule_id)
            if not db_validation:
                raise HTTPException(status_code=404, detail="Hero not found")
            data = rule.model_dump(exclude_unset=True)
            db_validation.sqlmodel_update(data)
            session.add(db_validation)
            await session.commit()
            await session.refresh(db_validation)
            return db_validation

    @staticmethod
    async def update_many(rules: list[RuleUpdateMany]) -> list[Rule]:
        updated_rules = []
        async with get_session() as session:
            for rule in rules:
                db_rule = await session.get(Rule, rule.id)
                if not db_rule:
                    raise HTTPException(status_code=404, detail=f"Rule with ID {rule.id} not found")
                data = rule.model_dump(exclude_unset=True)
                db_rule.sqlmodel_update(data)
                session.add(db_rule)
                updated_rules.append(db_rule)
            await session.commit()
            for db_rule in updated_rules:
                await session.refresh(db_rule)
        return updated_rules
