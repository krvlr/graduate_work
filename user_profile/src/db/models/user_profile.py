from db import Base
from uuid import UUID
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from models.user_profile import UserProfileSchema


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        unique=True,
        nullable=False,
        comment="Идентификатор пользователя"
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
    age: Mapped[int] = mapped_column(
        comment="Возраст пользователя"
    )
    first_name: Mapped[str] = mapped_column(
        comment="Имя пользователя"
    )
    last_name: Mapped[str] = mapped_column(
        comment="Второе имя пользователя"
    )
    country: Mapped[str] = mapped_column(
        comment="Страна пользователя"
    )
    city: Mapped[str] = mapped_column(
        comment="Город пользователя"
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
            city=self.city
        )
