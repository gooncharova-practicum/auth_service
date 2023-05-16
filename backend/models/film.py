from pydantic import UUID4

from models.base import OrjsonModel


class FilmGenre(OrjsonModel):
    id: UUID4
    name: str


class FilmPerson(OrjsonModel):
    id: UUID4
    name: str


class ESFilm(OrjsonModel):
    id: UUID4
    title: str
    imdb_rating: float
    description: str | None = None
    genre: list[FilmGenre]
    actors: list[FilmPerson] | None
    writers: list[FilmPerson] | None
    directors: list[FilmPerson] | None
