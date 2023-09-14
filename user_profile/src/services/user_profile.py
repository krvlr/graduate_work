from functools import lru_cache
from uuid import UUID

from models.user_profile import UserProfileRegisterSchemaRequest
from utils.unitofwork import IUnitOfWork


class UserProfileService:
    @staticmethod
    async def add_user_genre(
        unit_of_work: IUnitOfWork,
        user_id: UUID,
        user_preference: UserProfileRegisterSchemaRequest,
    ) -> tuple:
        async with unit_of_work:
            await unit_of_work.user_profile.read(id=user_id)

            try:
                genre = await unit_of_work.genre.read(name=user_preference.name)
                genre_id = genre.genre_id
            except Exception:
                genre_id = await unit_of_work.genre.create(data=user_preference.dict())

            await unit_of_work.user_profile_genre.create(
                data={"user_id": user_id, "genre_id": genre_id}
            )
            await unit_of_work.commit()
        return user_id, genre_id

    @staticmethod
    async def add_user(
        unit_of_work: IUnitOfWork,
        user_id: UUID,
        user_profile: UserProfileRegisterSchemaRequest,
    ) -> UUID:
        user_info = {"id": user_id} | user_profile.dict()

        async with unit_of_work:
            user_id = await unit_of_work.user_profile.create(data=user_info)
            await unit_of_work.commit()
        return user_id

    @staticmethod
    async def get_user(
        unit_of_work: IUnitOfWork,
        user_id: UUID,
    ) -> UUID:
        async with unit_of_work:
            user = await unit_of_work.user_profile.read(id=user_id)
        return user

    @staticmethod
    async def update_user(
        unit_of_work: IUnitOfWork,
        user_id: UUID,
        user_profile: UserProfileRegisterSchemaRequest,
    ) -> UUID:
        user = user_profile.dict()

        async with unit_of_work:
            user_id = await unit_of_work.user_profile.update(id=user_id, data=user)
            await unit_of_work.commit()
        return user_id

    @staticmethod
    async def delete_user(
        unit_of_work: IUnitOfWork,
        user_id: UUID,
    ) -> UUID:
        async with unit_of_work:
            user_id = await unit_of_work.user_profile.delete(id=user_id)
            await unit_of_work.commit()
        return user_id


@lru_cache()
def get_user_profile_service():
    user_profile_service = UserProfileService()
    return user_profile_service
