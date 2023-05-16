from abc import ABC, abstractmethod


class AsyncStorage(ABC):
    @abstractmethod
    async def get(self, _index: str, object_id: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def search(self, _index: str, data, **kwargs):
        raise NotImplementedError
