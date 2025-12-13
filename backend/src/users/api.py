from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from loguru import logger

from .crud import UserCRUD
from .models import UserShow, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/api/user/{user_id}", response_model=UserShow, tags=["Users"], summary="Get User by ID")
async def get_user(user_id: str) -> UserShow:
    logger.info(f"Get user endpoint called with user_id: {user_id}")

    user = await UserCRUD.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_show()


@router.get("/api/user/email/{email}", response_model=UserShow, tags=["Users"], summary="Get User by Email")
async def get_user_by_email(email: str) -> UserShow:
    logger.info(f"Get user by email endpoint called with email: {email}")

    user = await UserCRUD.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_show()


@router.get("/api/users", response_model=list[UserShow], tags=["Users"], summary="Get All Users")
async def get_all_users() -> list[UserShow]:
    logger.info("Get all users endpoint called")

    users = await UserCRUD.get_all()
    return [user.to_show() for user in users]


@router.put("/api/user/{user_id}", response_model=UserShow, tags=["Users"], summary="Update User")
async def update_user(user_id: str, user: UserUpdate) -> UserShow:
    logger.info(f"Update user endpoint called with user_id: {user_id} and data: {user}")

    user = await UserCRUD.update_one(user_id, user)
    return user.to_show()


@router.delete("/api/user/{user_id}", tags=["Users"], summary="Delete User")
async def delete_user(user_id: str) -> dict:
    logger.info(f"Delete user endpoint called with user_id: {user_id}")

    try:
        await UserCRUD.delete_one(user_id)
        return {"detail": "User deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user with user_id: {user_id} - {e}")
        return {"detail": "Error deleting user"}
