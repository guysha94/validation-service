from logging import DEBUG

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.models import ValidateRequest, ValidateResponse, CreateRulesRequest, CreateRulesResponse

api = FastAPI(

    name="Validation Service",
    debug=True,
    init_postgres=True,
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/health", tags=["Health"], summary="Health Check Endpoint")
async def health_check():
    """
    Health Check Endpoint to verify that the service is running.
    """
    logger.info("Health check endpoint called.")
    return {"status": "ok"}


@api.get("/")
async def root():
    return {"message": "Welcome to the Validation Service API"}


@api.post("/api/validate", tags=["Validation"], summary="Validate Data Endpoint")
async def validate_request(req: ValidateRequest) -> ValidateResponse:


    logger.info(f"Received validation request: {req}")

    return ValidateResponse(status="valid", errors=[])



@api.post("/api/create_rules", tags=["Rules"], summary="Create Rule Endpoint")
async def create_rule(req: CreateRulesRequest) -> CreateRulesResponse:
    logger.info(f"Create rule endpoint called with: {req}")

    dummy_response_id = [f"rule_{i}" for i in range(len(req.rules))]

    return CreateRulesResponse(
        success=True,
        created_rule_ids=dummy_response_id,
    )

def main():

    uvicorn.run(
        f"{__name__}:api",

        host="0.0.0.0",
        port=3001,
        reload=True,
        log_level=DEBUG,
        workers=1,
        use_colors=True,
    )
