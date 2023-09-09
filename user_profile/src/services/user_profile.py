from functools import lru_cache
from models.user_profile import UserProfileRegisterSchemaRequest
from uuid import UUID
from utils.unitofwork import IUnitOfWork
from sqlalchemy.exc import NoResultFound


class UserProfileService:
    @staticmethod
    async def add_user_genre(
        uow: IUnitOfWork,
        user_id: UUID,
        user_preference: UserProfileRegisterSchemaRequest,
    ) -> tuple:
        async with uow:
            await uow.user_profile.read(id=user_id)

            try:
                genre = await uow.genre.read(name=user_preference.name)
                genre_id = genre.genre_id
            except Exception:
                genre_id = await uow.genre.create(data=user_preference.dict())

            await uow.user_profile_genre.create(data={"user_id": user_id, "genre_id": genre_id})
            await uow.commit()
        return user_id, genre_id

    @staticmethod
    async def add_user(
        uow: IUnitOfWork,
        user_id: UUID,
        user_profile: UserProfileRegisterSchemaRequest,
    ) -> UUID:
        user_info = {"id": user_id} | user_profile.dict()

        async with uow:
            user_id = await uow.user_profile.create(data=user_info)
            await uow.commit()
        return user_id

    @staticmethod
    async def get_user(
        uow: IUnitOfWork,
        user_id: UUID,
    ) -> UUID:
        async with uow:
            user = await uow.user_profile.read(id=user_id)
        return user

    @staticmethod
    async def update_user(
        uow: IUnitOfWork,
        user_id: UUID,
        user_profile: UserProfileRegisterSchemaRequest,
    ) -> UUID:
        user = user_profile.dict()

        async with uow:
            user_id = await uow.user_profile.update(id=user_id, data=user)
            await uow.commit()
        return user_id

    @staticmethod
    async def delete_user(
        uow: IUnitOfWork,
        user_id: UUID,
    ) -> UUID:
        async with uow:
            user_id = await uow.user_profile.delete(id=user_id)
            await uow.commit()
        return user_id


@lru_cache()
def get_user_profile_service():
    user_profile_service = UserProfileService()
    return user_profile_service