import logging
from models.user_profile import (
    UserProfileRegisterSchemaRequest,
    UserProfileRegisterSchemaResponse,
    UserProfileSchema,
    UserProfileUpdateSchemaRequest,
    UserProfileUpdateSchemaResponse,
    UserGenreRegisterSchemaRequest,
)
from services.user_profile import UserProfileService, get_user_profile_service
from services.auth_service import JWTBearerService, get_jwt_bearer_service
from fastapi.security import HTTPBearer

from fastapi import APIRouter, Depends, status
from typing import Annotated
from utils.unitofwork import IUnitOfWork, UnitOfWork


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/register_user_genre", status_code=status.HTTP_201_CREATED)
async def register_user_genre(
    user_preference: UserGenreRegisterSchemaRequest,
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    user_id, genre_id = await user_profile_service.add_user_genre(
        uow=uow, user_id=user_id, user_preference=user_preference
    )
    return {"user_id": user_id, "genre_id": genre_id}


@router.post(
    "/register_user_profile",
    status_code=status.HTTP_201_CREATED,
    response_model=UserProfileRegisterSchemaResponse,
)
async def register_user_profile(
    user_profile: UserProfileRegisterSchemaRequest,
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    user_id = await user_profile_service.add_user(
        uow=uow, user_id=user_id, user_profile=user_profile
    )
    return {"user_id": user_id}


@router.put(
    "/update_user_profile",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileUpdateSchemaResponse,
)
async def update_user_profile(
    user_profile: UserProfileUpdateSchemaRequest,
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    user_id = await user_profile_service.update_user(
        uow=uow, user_id=user_id, user_profile=user_profile
    )
    return {"user_id": user_id}


@router.get(
    "/user_profile_details", status_code=status.HTTP_200_OK, response_model=UserProfileSchema
)
async def user_profile_details(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    user_info = await user_profile_service.get_user(uow=uow, user_id=user_id)
    return user_info


@router.delete("/delete_user_profile", status_code=status.HTTP_200_OK)
async def updated_user_profile(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
    user_profile_service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    user_id: Annotated[HTTPBearer, Depends(get_jwt_bearer_service())],
):
    user_id = await user_profile_service.delete_user(uow=uow, user_id=user_id)
    return {"user_id": user_id}