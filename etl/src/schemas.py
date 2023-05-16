from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel


class PGDataGenre(BaseModel):
    id: UUID
    name: str
    description: str | None
    modified: datetime


class PGDataFilmwork(BaseModel):
    id: UUID
    title: str
    description: str | None
    rating: int | None
    type: str
    created: datetime
    modified: datetime
    persons: list
    genres: list


class PGDataPerson(BaseModel):
    id: UUID
    full_name: str
    modified: datetime
