from abc import ABC, abstractmethod
from typing import Type
from db import async_session_maker
from db.repository.user_profile import (
    UserProfileRepository,
    GenreRepository,
    UserProfileGenreRepository,
)


class IUnitOfWork(ABC):
    user_profile: Type[UserProfileRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user_profile = UserProfileRepository(self.session)
        self.genre = GenreRepository(self.session)
        self.user_profile_genre = UserProfileGenreRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
