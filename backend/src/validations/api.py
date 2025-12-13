from fastapi import APIRouter
from loguru import logger

from .models import ValidateRequest, ValidateResponse

router = APIRouter(prefix="/api/validate", tags=["Validation"])

@router.post("/api/validate", tags=["Validation"], summary="Validate Data Endpoint")
async def validate_request(req: ValidateRequest) -> ValidateResponse:


    logger.info(f"Received validation request: {req}")

    return ValidateResponse(status="valid", errors=[])
