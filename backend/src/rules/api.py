from typing import Union

from fastapi import APIRouter, HTTPException
from loguru import logger

from .crud import RulesCRUD
from .models import Rule, RuleCreate, RuleUpdate, RuleUpdateMany

router = APIRouter(prefix="/api/rules", tags=["Rules"], )


@router.get("", tags=["Rules"], summary="Get All Rules Endpoint")
async def get_all_rules() -> list[Rule]:

    logger.info("Fetching all validations")

    return await RulesCRUD.get_all()


@router.post("", tags=["Rules"], summary="Create Validation Endpoint", response_model=Union[Rule, list[Rule]])
async def create_rules(rules: Union[RuleCreate, list[RuleCreate]]) -> Union[Rule, list[Rule]]:

    logger.info(f"Creating new rule(s): {rules}")
    if isinstance(rules, list):
        return await RulesCRUD.create_many(rules)
    else:
        return await RulesCRUD.create(rules)


@router.put("", tags=["Rules"], response_model=list[Rule], summary="Update Multiple Rules Endpoint")
async def update_multiple_rules(rules: list[RuleUpdateMany]) -> list[Rule]:

    logger.info(f"Updating multiple rules: {rules}")

    return await RulesCRUD.update_many(rules)


@router.get("/{rule_id}", tags=["Rules"], summary="Get Rule by ID Endpoint")
async def get_rule_by_id(rule_id: str) -> Rule:

    logger.info(f"Fetching rule with ID: {rule_id}")

    rule = await RulesCRUD.get_by_id(rule_id)
    if not rule:
        logger.error(f"Rule with ID {rule_id} not found")
        raise HTTPException(status_code=404, detail="Validation not found")
    return rule


@router.put("/{rule_id}", tags=["Rules"], summary="Update Validation Endpoint", response_model=Rule)
async def update_rule(rule_id: str, rule: RuleUpdate) -> Rule:

    logger.info(f"Updating rule with ID: {rule_id}")
    updated_validation = await RulesCRUD.update_one(rule_id, rule)
    if not updated_validation:
        logger.error(f"Validation with ID {rule_id} not found for update")
        raise HTTPException(status_code=404, detail="Validation not found")
    return updated_validation


@router.delete("/{rule_id}", tags=["Rules"], summary="Delete Validation Endpoint")
async def delete_rule(rule_id: str) -> dict[str, str]:

    logger.info(f"Deleting rule with ID: {rule_id}")
    await RulesCRUD.delete_one(rule_id)
    return {"detail": "Validation deleted successfully"}
