from core.config import postgres_settings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
async_engine = create_async_engine(postgres_settings.get_db_url())
async_session_maker = async_sessionmaker(bind=async_engine)


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=convention)

    def __repr__(self) -> str:
        columns = ", ".join(
            [f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"<{self.__class__.__name__}({columns})>"


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
