from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from .auth_bearer import JWTBearer
from .crud import TokenCRUD
from .models import LoginRequest, TokenData, TokenCreate, TokenShow, LoginResponse
from ..conf import settings
from ..services import AuthServiceDep, AuthService
from ..users.crud import UserCRUD
from ..users.models import User, UserCreate, UserShow, UserUpdate
from loguru import logger

router = APIRouter(prefix="/api/auth", tags=["Auth"])


async def get_current_user(token: Annotated[str, Depends(JWTBearer())]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = AuthService.decode_jwt(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError as e:
        raise credentials_exception from e
    user = await UserCRUD.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=TokenShow)
async def login_for_access_token(form_data: LoginRequest, auth_service: AuthServiceDep) -> TokenShow:
    user = await auth_service.authenticate_user(email=str(form_data.email), password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = await TokenCRUD.get_by_user_id(user_id=user.id)
    return token.to_show()


@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/verify-token", response_model=User)
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/refresh-token", response_model=TokenShow)
async def refresh_token(current_user: Annotated[User, Depends(get_current_active_user)],
                        auth_service: AuthServiceDep) -> TokenShow:
    access_token_expires = timedelta(minutes=settings.auth.expires_in_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(current_user.email)}, expires_delta=access_token_expires
    )
    await TokenCRUD.delete_by_user_id(user_id=current_user.id)
    token = await TokenCRUD.create(TokenCreate(access_token=access_token, user_id=current_user.id, token_type="bearer"))
    return token.to_show()


@router.post("/logout")
async def logout(current_user: Annotated[User, Depends(get_current_active_user)]) -> dict:
    await TokenCRUD.delete_by_user_id(user_id=current_user.id)
    return {"detail": "Logout successful"}


@router.post("/register", response_model=LoginResponse)
async def register_user(user: UserCreate, auth_service: AuthServiceDep) -> LoginResponse:
    existing_user = await UserCRUD.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = auth_service.get_password_hash(user.password)
    user.password = hashed_password
    user = await UserCRUD.create(user)
    access_token_expires = timedelta(minutes=settings.auth.expires_in_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.email)}, expires_delta=access_token_expires
    )

    token = await TokenCRUD.create(TokenCreate(access_token=access_token, user_id=user.id, token_type="bearer"))
    return LoginResponse(user=user.to_show(), access_token=token.access_token, token_type=token.token_type)


@router.post("/login", response_model=LoginResponse)
async def login_user(form_data: LoginRequest, auth_service: AuthServiceDep) -> LoginResponse:

    logger.info(f"Attempting login for email: {form_data.email}")
    user = await auth_service.authenticate_user(email=str(form_data.email), password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.auth.expires_in_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.email)}, expires_delta=access_token_expires
    )
    await TokenCRUD.delete_by_user_id(user_id=user.id)

    token = await TokenCRUD.create(TokenCreate(access_token=access_token, user_id=user.id, token_type="bearer"))
    return LoginResponse(user=user.to_show(), access_token=token.access_token, token_type=token.token_type)


@router.post("/change-password", response_model=UserShow)
async def change_password(
        current_user: Annotated[User, Depends(get_current_active_user)],
        new_password: str,
        auth_service: AuthServiceDep) -> UserShow:
    hashed_password = auth_service.get_password_hash(new_password)
    user = await UserCRUD.update_one(current_user.id, UserUpdate(password=hashed_password))
    return user.to_show()
