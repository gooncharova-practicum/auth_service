import abc
from typing import Any, Optional

import backoff
from aioredis import ConnectionError, Redis, TimeoutError

from config import max_waiting_time


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, key: str, value: Any) -> None:
        """Сохранить состояние в постоянное хранилище"""
        raise NotImplementedError("Method save_state is not defined")

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        raise NotImplementedError("Method retrieve_state is not defined")


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis) -> None:
        self.redis_adapter = redis_adapter

    @backoff.on_exception(
        backoff.expo, (ConnectionError, TimeoutError), max_time=max_waiting_time
    )
    async def save_state(self, key: str, value: Any) -> None:
        await self.redis_adapter.set(key, value)

    @backoff.on_exception(
        backoff.expo, (ConnectionError, TimeoutError), max_time=max_waiting_time
    )
    async def retrieve_state(self, key: str) -> Any:
        return await self.redis_adapter.get(key)


class State:
    """
    Класс для хранения состояния при работе с данными,
    чтобы постоянно не перечитывать данные с начала.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: str) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state(key, value)

    def get_state(self, key: str) -> Optional[str]:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state(key)
        if state:
            return state.decode("utf-8")
