import datetime
from typing import Tuple

from config import scheme_name
from schemas import PGDataGenre


def get_genre_sql_query(latest_record_time: datetime) -> str:
    """
    Формируем sql-запрос для жанров
    """

    return f"""SELECT id, "name", description, modified from {scheme_name}.genre
                   WHERE {scheme_name}.genre.modified > '{latest_record_time}';"""


def get_genre_data(row: dict, index_name: str) -> Tuple[PGDataGenre, dict, str]:
    data = PGDataGenre(**row)

    body = {
        "_index": index_name,
        "id": data.id,
        "name": data.name,
        "description": data.description,
    }

    string_for_log = "Genre"

    return data, body, string_for_log
