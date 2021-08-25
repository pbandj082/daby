from abc import ABCMeta, abstractmethod

from .pool import Pool


class Factory(metaclass=ABCMeta):
    async def create_pool(
        self,
        dsn: str,
        min_size: int = 10,
        max_size: int = 10,
    ) -> Pool:
        ...