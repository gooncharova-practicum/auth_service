import datetime
from typing import Tuple

from config import scheme_name
from schemas import PGDataPerson


def get_person_sql_query(latest_record_time: datetime) -> str:
    """
    Формируем sql-запрос для персон
    """

    return f"""SELECT id, "full_name", modified from {scheme_name}.person
                   WHERE {scheme_name}.person.modified > '{latest_record_time}';"""


def get_person_data(row: dict, index_name: str) -> Tuple[PGDataPerson, dict, str]:
    data = PGDataPerson(**row)
    body = {"_index": index_name, "id": data.id, "full": data.full_name}
    string_for_log = "Person"

    return data, body, string_for_log
