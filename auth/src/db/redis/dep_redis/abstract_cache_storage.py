from abc import ABC, abstractmethod


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get_record(self, key: str, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def set_record(self, key: str, value: str, expire: int, **kwargs):
        raise NotImplementedError()
