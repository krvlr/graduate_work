from typing import Type

from decorators import backoff
from pydantic import BaseModel


class DataTransform:
    @backoff()
    def validate_and_transform(
        self, model: Type[BaseModel], objects: list[dict]
    ) -> list[BaseModel]:
        return [model(**dict(obj)) for obj in objects]
