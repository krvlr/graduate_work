from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class UserProfileRegisterSchemaRequest(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: datetime

    @validator("age")
    def validate_age(cls, value):
        return value.replace(tzinfo=None)


class UserProfileRegisterSchemaResponse(BaseModel):
    user_id: UUID


class UserProfileSchema(BaseModel):
    user_id: UUID
    created: datetime
    modified: datetime
    first_name: str
    last_name: str
    country: str
    city: str
    age: datetime

    @validator("age")
    def validate_age(cls, value):
        return value.replace(tzinfo=None)


class UserProfileUpdateSchemaRequest(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: datetime

    @validator("age")
    def validate_age(cls, value):
        return value.replace(tzinfo=None)


class UserProfileUpdateSchemaResponse(BaseModel):
    user_id: UUID


class UserProfileDeleteSchemaResponse(BaseModel):
    user_id: UUID


class UserGenreRegisterSchemaRequest(BaseModel):
    name: str


class UserGenreRegisterSchemaResponse(BaseModel):
    genre_id: UUID
    user_id: UUID


class GenreSchema(BaseModel):
    genre_id: UUID
    name: str
