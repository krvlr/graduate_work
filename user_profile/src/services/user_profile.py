from functools import lru_cache
from db.repository.base import Repository
from models.user_profile import UserProfileRegisterSchemaRequest
from sqlalchemy.ext.asyncio import AsyncSession
from db.repository.user_profile import UserProfileRepository
from uuid import UUID


class UserProfileService:
    def __init__(self, user_profile_repo: Repository):
        self.user_profile_repo: Repository = user_profile_repo

    async def add_user(
        self,
        user_id: UUID,
        user_profile: UserProfileRegisterSchemaRequest,
        session: AsyncSession
    ) -> str:
        user_info = {"id": user_id} | user_profile.dict()
        user_id = await self.user_profile_repo.add(data=user_info, session=session)
        return user_id

    async def update_user(
        self,
        user_id: UUID,
        user_profile: UserProfileRegisterSchemaRequest,
        session: AsyncSession
    ) -> str:
        user_info = user_profile.dict()
        user_id = await self.user_profile_repo.update(model_id=user_id, data=user_info, session=session)
        return user_id

    async def get_user(
        self,
        user_id: UUID,
        session: AsyncSession
    ) -> dict:
        user_info = await self.user_profile_repo.get(model_id=user_id, session=session)
        return user_info

    async def delete_user(
        self,
        user_id: UUID,
        session: AsyncSession
    ) -> dict:
        user_id = await self.user_profile_repo.delete(model_id=user_id, session=session)
        return user_id


@lru_cache()
def get_user_profile_service():
    user_profile_repository = UserProfileRepository()
    user_profile_service = UserProfileService(user_profile_repo=user_profile_repository)
    return user_profile_service
