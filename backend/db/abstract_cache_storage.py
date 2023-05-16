from abc import ABC, abstractmethod


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        raise NotImplementedError()
