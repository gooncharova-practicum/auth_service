from functools import lru_cache
from typing import Union

from api.v1.utils import FilmParams, FilmSearchParams
from db import get_elastic, get_redis
from db.abstract_cache_storage import AsyncCacheStorage
from db.abstract_search_engine import AsyncStorage
from elasticsearch import NotFoundError
from fastapi import Depends
from models.film import ESFilm

from services.mixins import ServiceMixin

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(ServiceMixin):
    index_name = "movies"
    model = ESFilm
    search_fields = [
        "title^5",
        "description^4",
        "genres_titles^3",
        "actors_names^3",
        "writers_names^2",
        "directors",
    ]

    async def get_films(
        self, params: Union[FilmParams, FilmSearchParams]
    ) -> list[ESFilm] | None:
        body = self.es_request_body(params, self.search_fields)
        return await self.search_in_storage(body=body, schema=self.model)

    async def get_person_films(self, ids: list[str]):
        try:
            res = await self.storage.mget(body={"ids": ids}, index=self.index_name)
        except NotFoundError:
            return []
        return [self.model(**doc["_source"]) for doc in res["docs"]]


@lru_cache()
def get_film_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    storage: AsyncStorage = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache=cache, storage=storage, index="movies")
