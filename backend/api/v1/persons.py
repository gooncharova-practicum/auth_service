from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from services.person import PersonService, get_person_service

from api.v1.utils import validate_token

from .person_models import Person, PersonFilm

router = APIRouter(dependencies=[Depends(validate_token)])


@router.get(
    "/{person_id:uuid}/",
    response_model=Person,
    description="Get the Person projects which it works",
)
async def person_details(
    person_id: UUID4,
    page_size: int = 5,
    page_number: int = 0,
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    from_item = page_size * page_number
    result = await person_service.get_person_by_id(person_id, from_item, page_size)
    return result


@router.get(
    "/{person_id:uuid}/film",
    response_model=List[PersonFilm],
    description="Get all person's movies",
)
async def person_films_details(
    person_id: UUID4,
    page_size: int = 5,
    page_number: int = 0,
    person_service: PersonService = Depends(get_person_service),
) -> PersonFilm:
    from_item = page_size * page_number
    result = await person_service.get_person_films(person_id, from_item, page_size)
    return result


@router.get("/search/", response_model=List[Person], description="Search by the Person")
async def film_search(
    person_name: str,
    page_size: int = 5,
    page_number: int = 0,
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:
    from_item = page_size * page_number
    result = await person_service.search_person(person_name, from_item, page_size)
    return result
