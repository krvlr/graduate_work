from db.repository.base import SQLAlchemyRepository
from db.models.user_profile import UserProfile, Genre, UserProfileGenre


class UserProfileRepository(SQLAlchemyRepository):
    model = UserProfile
    name = "Профайл пользователя"


class GenreRepository(SQLAlchemyRepository):
    model = Genre
    name = "Жанр"


class UserProfileGenreRepository(SQLAlchemyRepository):
    model = UserProfileGenre
    name = "Связка пользователь предпочтительный жанр"
