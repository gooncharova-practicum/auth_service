from pydantic import UUID4, BaseModel


class Genre(BaseModel):
    """Модель для вывода жанров"""

    id: UUID4
    name: str
