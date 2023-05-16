from typing import Optional

from pydantic import UUID4

from models.base import OrjsonModel


class Genre(OrjsonModel):
    id: UUID4
    name: str
    description: Optional[str] = None
