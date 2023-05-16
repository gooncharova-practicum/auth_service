import time
from functools import lru_cache

from aioredis import Redis
from db import get_elastic, get_redis
from db.abstract_cache_storage import AsyncCacheStorage
from db.abstract_search_engine import AsyncStorage
from elasticsearch import AsyncElasticsearch, ConnectionError, TransportError
from fastapi import Depends
from models.genre import Genre
from pydantic import UUID4

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, cache: Redis, storage: AsyncElasticsearch):
        self.cache = cache
        self.storage = storage

    async def get_all_genres(self):
        query = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": [],
                    "filter": [{"match_all": {}}],
                }
            },
        }

        raw_data = await self.storage.search(index="genres", body=query)
        result = [
            {"id": i["_source"]["id"], "name": i["_source"]["name"]}
            for i in raw_data["hits"]["hits"]
        ]
        return result

    async def get_genre(self, resource_id: UUID4) -> Genre:
        query = {
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "bool": {
                                "should": [{"match_phrase": {"id": f"{resource_id}"}}],
                                "minimum_should_match": 1,
                            }
                        }
                    ],
                    "should": [],
                    "must_not": [],
                }
            }
        }

        raw_data = await self.storage.search(index="genres", body=query)
        return raw_data["hits"]["hits"][0]["_source"]


@lru_cache()
def get_genre_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    storage: AsyncStorage = Depends(get_elastic),
) -> GenreService:
    try:
        return GenreService(cache, storage)
    except (ConnectionError, TransportError):
        time.sleep(2)
