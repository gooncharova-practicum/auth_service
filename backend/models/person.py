from datetime import date

from pydantic import UUID4

from models.base import OrjsonModel


class Person(OrjsonModel):
    id: UUID4
    full_name: str
