from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.film import ESFilm
from pydantic import UUID4
from services.film import FilmService, get_film_service

from api.v1.film_models import FilmList, FilmModel
from api.v1.utils import FilmParams, validate_token

router = APIRouter(dependencies=[Depends(validate_token)])


@router.get(
    path="/",
    response_model=list[FilmList],
    summary="Get all movies",
    description="Get all movies",
)
async def film_list(
    params: FilmParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmModel]:
    es_films: list[FilmModel] = await film_service.get_films(params)
    if not es_films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Movies can not be taken from ElasticSearch.",
        )
    return [
        FilmModel(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description,
            genre=film.genre,
            actors=film.actors,
            writers=film.writers,
            directors=film.directors,
        )
        for film in es_films
    ]


@router.get(
    path="/{film_uuid}",
    response_model=FilmModel | None,
    summary="Searching movies by id",
    description="Searching movies by id",
)
async def film_details(
    film_uuid: UUID4, film_service: FilmService = Depends(get_film_service)
) -> FilmModel | None:
    film = await film_service.get_by_id(target_id=film_uuid, schema=ESFilm)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Film with uuid '{uuid}' was not found.".format(uuid=film_uuid),
        )
    return FilmModel(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )


@router.get(
    path="/search/",
    response_model=list[FilmList],
    summary="Searching movies",
    description="Searching movies",
)
async def film_search(
    params: FilmParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmModel]:
    es_films = await film_service.get_films(params)
    if not es_films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Can't find film with such query."
        )
    films = [
        FilmModel(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description,
            genre=film.genre,
            actors=film.actors,
            writers=film.writers,
            directors=film.directors,
        )
        for film in es_films
    ]
    return films
