import logging
from models.user_profile import (
    UserProfileRegisterSchemaRequest,
    UserProfileRegisterSchemaResponse,
    UserProfileSchema,
    UserProfileUpdateSchemaRequest,
    UserProfileUpdateSchemaResponse
)
from services.user_profile import UserProfileService, get_user_profile_service
from services.auth_service import JWTBearerService, get_jwt_bearer_service
from fastapi.security import HTTPBearer

from fastapi import APIRouter, Depends, status
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/register_user_profile",
    status_code=status.HTTP_201_CREATED,
    response_model=UserProfileRegisterSchemaResponse
)
async def register_user_profile(
    user_profile: UserProfileRegisterSchemaRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())]
):
    user_id = await user_profile_service.add_user(user_id=user_id, user_profile=user_profile, session=session)
    return {"user_id": user_id}


@router.put(
    "/update_user_profile",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileUpdateSchemaResponse
)
async def update_user_profile(
    user_profile: UserProfileUpdateSchemaRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())]
):
    user_id = await user_profile_service.update_user(user_id=user_id, user_profile=user_profile, session=session)
    return {"user_id": user_id}


@router.get(
    "/user_profile_details",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileSchema
)
async def user_profile_details(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())]
):
    user_info = await user_profile_service.get_user(user_id=user_id, session=session)
    return user_info


@router.delete(
    "/delete_user_profile",
    status_code=status.HTTP_200_OK
)
async def updated_user_profile(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())]
):
    user_id = await user_profile_service.delete_user(user_id=user_id, session=session)
    return {"user_id": user_id}
