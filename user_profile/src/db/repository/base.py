from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi import status, HTTPException
from sqlalchemy.exc import NoResultFound


class IRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def read(self, **filter_by) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, data: dict) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> UUID:
        raise NotImplementedError


class SQLAlchemyRepository(IRepository):
    model = None
    name = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> UUID:
        model_info = await self.session.execute(select(self.model.id).filter_by(**data))  # type: ignore[attr-defined]

        if model_info.all():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке регистрации. {self.name} уже зарегистирован.",
            )

        query = insert(self.model).values(**data).returning(self.model.id)  # type: ignore[attr-defined]
        result = await self.session.execute(query)
        return result.scalar_one()

    async def read(self, **filter_by) -> dict:
        try:
            model_info = await self.session.execute(select(self.model).filter_by(**filter_by))
            return model_info.scalar_one().to_read()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке получить детальную информацию. {self.name} не зарегистирован.",
            )

    async def update(self, id: UUID, data: dict) -> UUID:
        model_info = await self.session.execute(select(self.model.id).filter_by(**data))  # type: ignore[attr-defined]

        if not model_info.all():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке обновления. {self.name} не зарегистирован.",
            )

        query = (
            update(self.model).where(
                self.model.id == id
            ).values(**data).returning(self.model.id)  # type: ignore[attr-defined]
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete(self, id: UUID) -> UUID:
        try:
            query = delete(self.model).where(self.model.id == id).returning(self.model.id)  # type: ignore[attr-defined]
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при попытке удалить информацию. {self.name} не зарегистирован.",
            )
