from fastapi import APIRouter, HTTPException
from loguru import logger

from .crud import ValidationCRUD
from .models import ValidateRequest, ValidateResponse, Validation, ValidationCreate, ValidationUpdate

router = APIRouter(prefix="/api/validations", tags=["Validations"])


@router.post("/validate", tags=["Validations"], summary="Validate Data Endpoint")
async def validate_request(req: ValidateRequest) -> ValidateResponse:

    logger.info(f"Received validation request: {req}")

    return ValidateResponse(status="valid", errors=[])


@router.get("", tags=["Validations"], summary="Get All Validations Endpoint")
async def get_all_validations() -> list[Validation]:

    logger.info("Fetching all validations")

    return await ValidationCRUD.get_all()


@router.get("/{validation_id}", tags=["Validations"], summary="Get Validation by ID Endpoint")
async def get_validation_by_id(validation_id: str) -> Validation:

    logger.info(f"Fetching validation with ID: {validation_id}")

    validation = await ValidationCRUD.get_by_id(validation_id)
    if not validation:
        logger.error(f"Validation with ID {validation_id} not found")
        raise HTTPException(status_code=404, detail="Validation not found")
    return validation


@router.post("", tags=["Validations"], summary="Create Validation Endpoint")
async def create_validation(validation: ValidationCreate) -> Validation:

    logger.info(f"Creating new validation: {validation}")
    return await ValidationCRUD.create(validation)


@router.delete("/validations/{validation_id}", tags=["Validations"], summary="Delete Validation Endpoint")
async def delete_validation(validation_id: str) -> dict[str, str]:

    logger.info(f"Deleting validation with ID: {validation_id}")
    await ValidationCRUD.delete_one(validation_id)
    return {"detail": "Validation deleted successfully"}


@router.put("/{validation_id}", tags=["Validations"], summary="Update Validation Endpoint")
async def update_validation(validation_id: str, validation: ValidationUpdate) -> Validation:

    logger.info(f"Updating validation with ID: {validation_id}")
    updated_validation = await ValidationCRUD.update_one(validation_id, validation)
    if not updated_validation:
        logger.error(f"Validation with ID {validation_id} not found for update")
        raise HTTPException(status_code=404, detail="Validation not found")
    return updated_validation
