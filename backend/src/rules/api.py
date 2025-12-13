from fastapi import APIRouter
from loguru import logger

from .models import CreateRulesRequest, CreateRulesResponse

router = APIRouter(prefix="/api/rules", tags=["Rules"], )


@router.post("/api/create_rules", tags=["Rules"], summary="Create Rule Endpoint")
async def create_rule(req: CreateRulesRequest) -> CreateRulesResponse:
    logger.info(f"Create rule endpoint called with: {req}")

    dummy_response_id = [f"rule_{i}" for i in range(len(req.rules))]

    return CreateRulesResponse(
        success=True,
        created_rule_ids=dummy_response_id,
    )
