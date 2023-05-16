from pydantic import UUID4, BaseModel


class Person(BaseModel):
    """Модель для описания участника в фильме"""

    id: UUID4
    name: str


class Genre(BaseModel):
    """Модель для описания жанра в фильме"""

    id: UUID4
    name: str


class FilmModel(BaseModel):
    """Модель для вывода информации о фильме"""

    id: UUID4
    title: str
    imdb_rating: float
    description: str | None = None
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]


class FilmList(BaseModel):
    """Модель для вывода списка фильмов"""

    id: UUID4
    title: str
    imdb_rating: float
