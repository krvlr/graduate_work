from db import Base
from uuid import uuid4, UUID
from sqlalchemy import func, ForeignKey
from datetime import datetime, date
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship
from models.user_profile import UserProfileSchema, GenreSchema


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, nullable=False, comment="Идентификатор пользователя"
    )
    created: Mapped[datetime] = mapped_column(
        comment="Время создания записи",
        default=func.now(),
        nullable=False,
    )
    modified: Mapped[datetime] = mapped_column(
        comment="Время изменения записи",
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    age: Mapped[date] = mapped_column(comment="Дата рождения пользователя")
    first_name: Mapped[str] = mapped_column(comment="Имя пользователя")
    last_name: Mapped[str] = mapped_column(comment="Второе имя пользователя")
    country: Mapped[str] = mapped_column(comment="Страна пользователя")
    city: Mapped[str] = mapped_column(comment="Город пользователя")
    genres: WriteOnlyMapped[list["Genre"]] = relationship(
        secondary="user_profile_genre", back_populates="users"
    )

    def to_read(self):
        return UserProfileSchema(
            user_id=self.id,
            age=self.age,
            created=self.created,
            modified=self.modified,
            first_name=self.first_name,
            last_name=self.last_name,
            country=self.country,
            city=self.city,
        )


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid4, unique=True, nullable=False, comment="Идентификатор жанра"
    )
    name: Mapped[str] = mapped_column(unique=True, nullable=False, comment="Название жанра")
    users: WriteOnlyMapped[list["UserProfile"]] = relationship(
        secondary="user_profile_genre", back_populates="genres"
    )

    def to_read(self):
        return GenreSchema(
            genre_id=self.id,
            name=self.name,
        )


class UserProfileGenre(Base):
    __tablename__ = "user_profile_genre"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
        comment="Идентификатор связи пользователя и жанра",
    )
    created: Mapped[datetime] = mapped_column(
        comment="Время создания записи",
        default=func.now(),
        nullable=False,
    )
    modified: Mapped[datetime] = mapped_column(
        comment="Время изменения записи",
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_profile.id", ondelete="CASCADE"), comment="Идентификатор пользователя"
    )
    genre_id: Mapped[UUID] = mapped_column(
        ForeignKey("genre.id", ondelete="CASCADE"), comment="Идентификатор жанра"
    )
