from abc import ABCMeta, abstractmethod
from typing import Optional

from .connection import Connection


class PoolAcquireContext(metaclass=ABCMeta):
    @abstractmethod
    async def __aenter__(self) -> Connection:
        ...
    
    @abstractmethod
    async def __aexit__(self) -> None:
        ...


class Pool(metaclass=ABCMeta):
    @abstractmethod
    def acquire(
        self,
        timeout: Optional[int] = None
    ) -> PoolAcquireContext:
        ...

    @abstractmethod
    async def close() -> None:
        ...
