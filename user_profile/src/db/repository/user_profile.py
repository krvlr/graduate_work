from db.repository.base import SQLAlchemyRepository
from db.models.user_profile import UserProfile


class UserProfileRepository(SQLAlchemyRepository):
    model = UserProfile
    name = "профайл пользователя"
