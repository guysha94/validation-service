from fastapi import APIRouter
from loguru import logger
from python_sdk.domain import APIHealthResponse
from starlette.responses import RedirectResponse

router = APIRouter(prefix="", tags=["Health"])


@router.get("/health", tags=["Health"], summary="Health Check Endpoint")
async def health_check():
    """
    Health Check Endpoint to verify that the service is running.
    """
    logger.info("Health check endpoint called.")
    return APIHealthResponse()


@router.get("/healthz", tags=["Health"], summary="Health Check Endpoint")
async def healthz_check():
    """
    Health Check Endpoint to verify that the service is running.
    """
    return RedirectResponse(url="/health")
