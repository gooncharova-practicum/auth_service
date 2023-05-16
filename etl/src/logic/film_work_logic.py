from contextlib import closing, contextmanager
from datetime import datetime
from logging import getLogger
from time import sleep

import psycopg2
import psycopg2.extras
from elasticsearch import Elasticsearch, helpers
from pydantic import BaseModel
from retry import retry

from config import (
    date_format,
    default_modified,
    postgres_config,
    elastic_config,
    index_name as config_index_name,
)
from logic import film_work_logic, genre_logic, person_logic
from state_saver import State

logger = getLogger()


def latest_tmstp(state: State, short_name: str) -> datetime:
    last_modified_datetime = state.get_state(f"{short_name}_modified")
    if not last_modified_datetime:
        last_modified_datetime = default_modified
    latest_record_time = datetime.strptime(last_modified_datetime, date_format)
    return latest_record_time


def get_sql_query(short_name: str, latest_record_time: datetime) -> str:
    """
    Получаем sql-запрос в зависимости от short_name
    """
    if short_name == "genres_only":
        return genre_logic.get_genre_sql_query(latest_record_time)

    if short_name == "persons_only":
        return person_logic.get_person_sql_query(short_name, latest_record_time)

    return film_work_logic.get_filmwork_sql_query(latest_record_time, short_name)


def sql_data(short_name: str, batch_size: int, state: State) -> BaseModel:
    """
    Получение данных из Postgres с помощью генератора
    """
    with psycopg2.connect(postgres_config.ELST_DB_DSN) as pg_conn, closing(
        pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    ) as curs:
        latest_record_time = latest_tmstp(state, short_name)
        sql_query = get_sql_query(short_name, latest_record_time)
        try:
            curs.execute(sql_query)
            while True:
                data = curs.fetchmany(size=batch_size)
                if data:
                    yield data
                else:
                    break
        except Exception as e:
            logger.exception(f"We have the following trouble connection: {e}")


def es_bulk_prepare(
    rows_batch: tuple,
    short_name: str,
    index_name: str,
    tries_latency: float,
    state: State,
):
    if short_name == "genres_only":
        get_body_func = genre_logic.get_genre_data
    elif short_name == "persons_only":
        get_body_func = person_logic.get_person_data
    else:
        get_body_func = film_work_logic.get_filmwork_data

    for row in rows_batch:
        latest_record_time = latest_tmstp(state, short_name)
        data, body, string_for_log = get_body_func(row, index_name)

        if data.modified > latest_record_time or not latest_record_time:
            time = str(data.modified)
            state.set_state(f"{short_name}_modified", time)
            logger.info(f"{string_for_log} added - {data.modified} {data.title}")
            sleep(tries_latency)

            yield body


@contextmanager
def elasticsearch_context(elastic_host, elastic_port):
    es = Elasticsearch(host=elastic_host, port=elastic_port)
    yield es
    es.transport.close()


@retry(exceptions=Exception, tries=-1, delay=0.1, max_delay=10, jitter=1)
def transformator_pg_es(
    short_name: str,
    batch_size: int,
    state: State,
    tries_latency: float = 0,
) -> int:
    """
    Копирование полученных данных из Postgres в Elasticsearch
    """
    with elasticsearch_context(
        elastic_config.ELASTIC_HOST, elastic_config.ELASTIC_PORT
    ) as es:
        for rows_batch in sql_data(short_name, batch_size, state):
            helpers.bulk(
                es,
                es_bulk_prepare(
                    rows_batch, short_name, config_index_name, tries_latency, state
                ),
            )
