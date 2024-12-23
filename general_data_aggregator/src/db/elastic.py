import logging
import re
from copy import deepcopy
from enum import Enum
from typing import Any, Type, Optional

from elasticsearch import NotFoundError, AsyncElasticsearch
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass

from models.movie import ElasticMovieBrief

logger = logging.getLogger(__name__)

client: Optional[AsyncElasticsearch] = None


def get_elastic_client() -> AsyncElasticsearch:
    return client


class SortingOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class ObjectName(Enum):
    MOVIES = "movies"


class ElasticAdapter:
    def __init__(self, data_provider: AsyncElasticsearch, allowed_sort_fields: dict):
        self.data_provider = data_provider
        self.allowed_sort_fields = allowed_sort_fields

    async def get_object_by_id(
        self,
        obj_id: str,
        obj_name: ObjectName,
        model_cls: Type[ElasticMovieBrief],
    ) -> BaseModel | None:
        try:
            doc = await self.data_provider.get(obj_name.value, obj_id)
        except NotFoundError:
            return None
        return model_cls(**doc["_source"])

    async def search(
        self,
        obj_name: ObjectName,
        model: Type[BaseModel],
        page_number: int,
        page_size: int,
        sort: list[str] | None = None,
        filters: dict[str, list] | None = None,
        query: str | None = None,
    ) -> list[BaseModel]:
        logger.debug(f"In ElasticAdapter method search, query = {query}")

        if query:
            body: dict = {"query": {"bool": {"must": {}}}}

            for _query in query.split(","):
                field = re.split(">=|<=|>|<|=", _query)[0]
                body["query"]["bool"]["must"]["match"] = {
                    field: {"query": _query, "fuzziness": "auto"}
                }

        else:
            body = {"query": {"bool": {"must": {"match_all": {}}}}}

        filters = {k: v for k, v in filters.items() if v is not None} if filters else dict()

        body = self._add_query_filters(body, filters, model)
        logger.debug(f"Elastic query: {body}")

        try:
            docs = await self.data_provider.search(
                index=obj_name.value,
                body=body,
                from_=page_number * page_size,
                size=page_size,
                sort=self._make_sort_string(sort, model),
            )
        except NotFoundError:
            return []

        return [model(**doc["_source"]) for doc in docs["hits"]["hits"]]

    def _make_sort_string(self, sort_fields: list[str] | None, model: Type[BaseModel]) -> str:
        if sort_fields is None:
            return "id:desc"

        prepared_sort_fields = []
        for field in sort_fields:
            sort_order = (
                SortingOrder.DESC.value if field.startswith("-") else SortingOrder.ASC.value
            )
            sort_by = field.strip("-")
            if sort_by in model.model_fields and sort_by in self.allowed_sort_fields:
                prepared_sort_fields.append(
                    f"{sort_by}{'.raw' if self.allowed_sort_fields[sort_by] == str else ''}"
                    f":{sort_order}"
                )
        logger.debug(f"Elastic sorting: {','.join(prepared_sort_fields)}")
        return ",".join(prepared_sort_fields)

    def _add_query_filters(self, query: dict, filters: dict, model: Type[BaseModel]) -> dict:
        query_filters = list()

        for filter_field, values in filters.items():
            if path := self._generate_filter_path(filter_field, model):
                query_filter = self._generate_filter(path, values)
                query_filters.append(query_filter)

        if query_filters:
            query["query"]["bool"]["filter"] = query_filters

        return query

    @staticmethod
    def _generate_filter(path: list, values: Any):
        inner_insert = {"nested": {"path": str(), "query": {}}}
        curr: dict = dict()

        for i in range(1, len(path)):
            curr.update(deepcopy(inner_insert))
            curr["nested"]["path"] = ".".join(path[:i])
            curr = curr["nested"]["query"]
        curr.update({"terms": {".".join(path): values}})

        return curr

    @staticmethod
    def _generate_filter_path(filter_path: str, root_model: Type[BaseModel]):
        path = list()
        while filter_path:
            path_field = str()

            for field_name, field in root_model.model_fields.items():
                if filter_path.startswith(field_name):
                    path_field = field_name
                    filter_path = filter_path.lstrip(field_name).lstrip("_")

                    if isinstance(field.type_, ModelMetaclass):
                        root_model = field.type_

            if not path_field:
                logger.warning(f"Invalid filter path: {filter_path}")
                return

            path.append(path_field)

        return path


def get_elastic_adapter() -> ElasticAdapter:
    return ElasticAdapter(get_elastic_client(), {})
