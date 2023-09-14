from db.models.user_profile import Genre, UserProfile, UserProfileGenre
from db.repository.base import SQLAlchemyRepository


class UserProfileRepository(SQLAlchemyRepository):
    model = UserProfile
    name = "Профайл пользователя"


class GenreRepository(SQLAlchemyRepository):
    model = Genre
    name = "Жанр"


class UserProfileGenreRepository(SQLAlchemyRepository):
    model = UserProfileGenre
    name = "Связка пользователь предпочтительный жанр"
