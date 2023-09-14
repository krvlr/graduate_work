from datetime import date
from uuid import UUID

from pydantic import BaseModel


class UserProfile(BaseModel):
    user_id: UUID
    age: date
    first_name: str
    last_name: str
    country: str
    city: str
    genres: list

    def get_key(self):
        return f"{str(self.user_id)}:user_profile"

    def get_value(self):
        return {
            "age": str(self.age),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "country": self.country,
            "city": self.city,
            "genres": self.genres,
        }

    def transform(self):
        return self.get_key(), self.get_value()
