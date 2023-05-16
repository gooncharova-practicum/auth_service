import time
from typing import Union

from aioredis import Redis
from api.v1.utils import FilmParams, FilmSearchParams
from elasticsearch import (
    AsyncElasticsearch,
    ConnectionError,
    NotFoundError,
    TransportError,
)
from models.film import ESFilm
from models.genre import Genre
from models.person import Person
from pydantic import UUID4
from pydantic.main import BaseModel

Schemas = (ESFilm, Person, Genre)
ES_schemas = Union[ESFilm, Person, Genre]


class CacheValue(BaseModel):
    name: str
    value: str


class ServiceMixin:
    def __init__(self, cache: Redis, storage: AsyncElasticsearch, index: str):
        self.cache = cache
        self.storage = storage
        self.index = index

    async def _build_cache_key(self, cache_values: list[CacheValue]) -> str:
        separate = "::"
        key = f"{self.index}{separate}"
        for v in cache_values:
            key += f"{v.name}{separate}{v.value}"
        return key

    async def search_in_storage(self, body: dict, schema: Schemas) -> ES_schemas | None:
        try:
            docs = await self.storage.search(index=self.index, body=body)
            return [schema(**row["_source"]) for row in docs["hits"]["hits"]]
        except (ConnectionError, TransportError):
            time.sleep(2)
        except NotFoundError:
            return None

    async def get_by_id(self, target_id: UUID4, schema: Schemas) -> ES_schemas | None:
        cache_key = await self._build_cache_key(
            [CacheValue(name="person_id", value=str(target_id))]
        )
        instance = await self._get_result_from_cache(cache_key)
        if not instance:
            instance = await self._get_data_from_storage_by_id(target_id=target_id, schema=schema)
            if not instance:
                return None
            await self._put_data_to_cache(key=cache_key, instance=instance.json())
            return instance
        return schema.parse_raw(instance)

    async def _get_data_from_storage_by_id(
        self, target_id: str, schema: Schemas
    ) -> ES_schemas | None:
        try:
            body = {"query": {"match_phrase": {"id": target_id}}}
            doc = await self.storage.search(index=self.index, body=body)
            return schema(**doc["hits"]["hits"][0]["_source"])
        except NotFoundError:
            return None

    async def _get_result_from_cache(self, key: str) -> bytes | None:
        data = await self.cache.get(key)
        return data or None

    async def _put_data_to_cache(self, key: str, instance: Union[bytes, str]) -> None:
        await self.cache.set(key, instance, 20)

    def es_request_body(
        self,
        params: Union[FilmParams, FilmSearchParams],
        search_fields: list[str] | None,
    ) -> dict:
        if isinstance(params, FilmParams):
            if params.filter_genre_id:
                return {
                    "size": params.size,
                    "from": (params.number - 1) * params.size,
                    "query": {
                        "nested": {
                            "path": "genre",
                            "query": {"match": {"genre.id": params.filter_genre_id}},
                        }
                    },
                }
            else:
                return {
                    "size": params.size,
                    "from": (params.number - 1) * params.size,
                    "query": {"match_all": {}},
                }
        elif isinstance(params, FilmSearchParams):
            return {
                "size": params.size,
                "from": (params.number - 1) * params.size,
                "query": {
                    "multi_match": {
                        "query": params.query,
                        "fuzziness": "auto",
                        "fields": search_fields,
                    }
                },
            }
        else:
            return {
                "size": params.size,
                "from": (params.number - 1) * params.size,
                "query": {"match_all": {}},
            }
