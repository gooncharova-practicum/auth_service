from enum import Enum
from typing import List

from pydantic import UUID4, BaseModel


class RoleType(Enum):
    """Роли в фильме"""

    actor = "actor"
    director = "director"
    writer = "writer"


class PersonFilmShort(BaseModel):
    """Модель, для вывода фильмов, в которых
    принимала участие персона + ее роль в фильме"""

    uuid: UUID4
    roles: List[RoleType]


class Person(BaseModel):
    """Модель для вывода участников фильма"""

    uuid: UUID4
    full_name: str
    films: List[PersonFilmShort]


class PersonFilm(BaseModel):
    """Модель для вывода фильма, в котором учавствовала персона"""

    uuid: UUID4
    title: str
    imdb_rating: float
