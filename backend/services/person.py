from functools import lru_cache

from aioredis import Redis
from db import get_elastic, get_redis
from db.abstract_cache_storage import AsyncCacheStorage
from db.abstract_search_engine import AsyncStorage
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from pydantic import UUID4

from .queries_list import QueriesList

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, cache: Redis, storage: AsyncElasticsearch):
        self.cache = cache
        self.storage = storage
        self.queries_list = QueriesList()

        self.roles = ["writers_names", "actors_names", "director"]
        self.roles_maping = {
            "director": "director",
            "writers_names": "writer",
            "actors_names": "actor",
        }

    async def person_searcher(self, person: dict, from_item: int, page_size: int):
        p_name = person["full_name"]
        p_id = person["id"]
        film_info_list = []
        x = await self.storage.search(
            index="movies",
            body=self.queries_list.get_person_film(
                p_name,
                from_item,
                page_size,
            ),
        )
        for n in x["hits"]["hits"]:
            roles_list = []
            m = n["_source"]

            roles_list = [
                self.roles_maping[k]
                for k, v in m.items()
                if k in self.roles
                if p_name in v
            ]
            film_info = {"uuid": m["id"], "roles": roles_list}
            film_info_list.append(film_info)
        d_result = {"uuid": p_id, "full_name": p_name, "films": film_info_list}
        return d_result

    async def search_person(self, person_name: str, from_item: int, page_size: int):
        person_data = await self.storage.search(
            index="persons", body=self.queries_list.get_person_by_name(person_name)
        )
        person_collection = [i["_source"] for i in person_data["hits"]["hits"]]
        main_result = []
        for person in person_collection:
            d_result = await self.person_searcher(person, from_item, page_size)
            main_result.append(d_result)
        return main_result

    async def get_person_by_id(self, person_id: UUID4, from_item: int, page_size: int):
        person = (
            await self.storage.search(
                index="persons", body=self.queries_list.get_person_by_uuid(person_id)
            )
        )["hits"]["hits"][0]["_source"]

        return await self.person_searcher(person, from_item, page_size)

    async def get_person_films(self, person_id: UUID4, from_item: int, page_size: int):
        person = (
            await self.storage.search(
                index="persons", body=self.queries_list.get_person_by_uuid(person_id)
            )
        )["hits"]["hits"][0]["_source"]

        p_name = person["full_name"]
        film_info_list = []
        x = await self.storage.search(
            index="movies",
            body=self.queries_list.get_person_film(
                p_name,
                from_item,
                page_size,
            ),
        )
        for n in x["hits"]["hits"]:
            m = n["_source"]
            film_obj = {
                "uuid": m["id"],
                "title": m["title"],
                "imdb_rating": m["imdb_rating"],
            }
            film_info_list.append(film_obj)
        return film_info_list


@lru_cache()
def get_person_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    elastic: AsyncStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, elastic)
