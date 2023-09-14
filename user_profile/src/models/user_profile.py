from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class UserProfileRegisterSchemaRequest(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: date


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
    age: date


class UserProfileUpdateSchemaRequest(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: date


class UserProfileUpdateSchemaResponse(BaseModel):
    user_id: UUID


class GenreSchema(BaseModel):
    genre_id: UUID
    name: str


class GenreSchemaRequest(BaseModel):
    genre_id: UUID
    name: str


class GenreSchemaResponse(BaseModel):
    genre_id: UUID
    user_id: UUID


class UserGenreRegisterSchemaRequest(BaseModel):
    name: str
