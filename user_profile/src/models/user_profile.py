from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserProfileRegisterSchemaRequest(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: int


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
    age: int


class UserProfileUpdateSchemaRequest(BaseModel):
    first_name: str
    last_name: str
    country: str
    city: str
    age: int


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
