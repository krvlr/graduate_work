from datetime import date, datetime, timedelta
from uuid import UUID, uuid4

from db import Base
from models.user_profile import GenreSchema, UserProfileSchema
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, nullable=False, comment="Идентификатор пользователя"
    )
    created: Mapped[datetime] = mapped_column(
        comment="Время создания записи",
        default=func.now() + timedelta(hours=3),
        nullable=False,
    )
    modified: Mapped[datetime] = mapped_column(
        comment="Время изменения записи",
        default=func.now() + timedelta(hours=3),
        onupdate=func.now() + timedelta(hours=3),
        nullable=False,
    )
    age: Mapped[datetime] = mapped_column(comment="Дата рождения пользователя")
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
        default=func.now() + timedelta(hours=3),
        nullable=False,
    )
    modified: Mapped[datetime] = mapped_column(
        comment="Время изменения записи",
        default=func.now() + timedelta(hours=3),
        onupdate=func.now() + timedelta(hours=3),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_profile.id", ondelete="CASCADE"), comment="Идентификатор пользователя"
    )
    genre_id: WriteOnlyMapped[UUID] = mapped_column(
        ForeignKey("genre.id", ondelete="CASCADE"), comment="Идентификатор жанра"
    )
