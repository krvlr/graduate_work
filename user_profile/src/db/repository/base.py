from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import status, HTTPException
from sqlalchemy.exc import NoResultFound
import uuid


class Repository(ABC):
    @abstractmethod
    async def add(self, data: dict, session: AsyncSession) -> str:
        raise NotImplementedError

    @abstractmethod
    async def update(self, model_id: UUID, data: dict, session: AsyncSession) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get(self, model_id: UUID, session: AsyncSession) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, model_id: UUID, session: AsyncSession) -> dict:
        raise NotImplementedError


class SQLAlchemyRepository(Repository):
    model = None
    name = None

    async def add(self, data: dict, session: AsyncSession) -> str:
        model_info = await session.execute(select(self.model.id).where(self.model.id == data["id"]))

        if model_info.all():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке регистрации, {self.name} c id = {data['id']} уже зарегистирован."
            )

        query = insert(self.model).values(**data).returning(self.model.id)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one()

    async def update(self, model_id: UUID, data: dict, session: AsyncSession) -> str:
        model_info = await session.execute(select(self.model.id).where(self.model.id == model_id))

        if not model_info.all():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке обновления, {self.name} c id = {model_id} не зарегистирован."
            )

        query = update(self.model).where(self.model.id == model_id).values(**data).returning(self.model.id)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one()

    async def get(self, model_id: UUID, session: AsyncSession) -> dict:
        try:
            model_info = await session.execute(select(self.model).where(self.model.id == model_id))
            return model_info.one()[0].to_read()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке получить детальную информацию, "
                       f"{self.name} c id = {model_id} не зарегистирован."
            )

    async def delete(self, model_id: UUID, session: AsyncSession) -> dict:
        try:
            query = delete(self.model).where(self.model.id == model_id).returning(self.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке удалить информацию, "
                       f"{self.name} c id = {model_id} не зарегистирован."
            )
