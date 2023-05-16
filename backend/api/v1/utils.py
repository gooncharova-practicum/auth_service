from functools import wraps
from http import HTTPStatus

import requests
from core import auth_config
from fastapi import Header, HTTPException


class FilmSearchParams:
    """Params for film searching"""

    def __init__(
        self,
        query: str
        | None = Query(
            None,
            alias="query",
            title="Query",
            description="Searching by movie name",
        ),
        num: int
        | None = Query(
            1,
            alias="page[number]",
            title="page",
            description="Page number",
            ge=1,
        ),
        size: int
        | None = Query(
            50,
            alias="page[size]",
            title="page size",
            description="Num of documents in page",
            ge=1,
        ),
    ) -> None:
        self.query = query
        self.number = num
        self.size = size


class FilmParams:
    """Params for movie output"""

    def __init__(
        self,
        filter_genre_id: str
        | None = Query(
            None,
            alias="filter[genre]",
            title="Genre filter",
            description="Filtring movies by genres",
        ),
        num: int
        | None = Query(
            1,
            alias="page[number]",
            title="page",
            description="Page number",
            ge=1,
        ),
        size: int
        | None = Query(
            50,
            alias="page[size]",
            title="size of page",
            description="Num of documents in page",
            ge=1,
        ),
    ) -> None:
        self.filter_genre_id = filter_genre_id
        self.number = num
        self.size = size


async def validate_token(authorization: str = Header("Authorization")):
    token = authorization
    url = f"{auth_config.HOST}:{auth_config.PORT}{auth_config.URL_PREFIX}{auth_config.TOKEN_VALIDATE_ENDPOINT}"
    data = {"token": token}
    res = await requests.post(url, data=data)
    if not res:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Token has expired",
        )
