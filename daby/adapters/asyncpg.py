import asyncpg

from ..connection import Connection
from ..exceptions import PoolConnectionError
from ..pool import Pool, PoolAcquireContext


class AsyncpgConnection(Connection):
    def __init__(self, origin: asyncpg.Connection):
        self._origin = origin


class AsyncpgPoolAcquireContext(PoolAcquireContext):
    def __init__(self, origin: asyncpg.pool.PoolAcquireContext):
        self._origin = origin
    
    async def __aenter__(self) -> Connection:
        origin_connection = await self._origin.__aenter__()
        connection = AsyncpgConnection(origin=origin_connection)
        return connection


    async def __aexit__(self) -> None:
        await self._origin.__aexit__()


class AsyncpgPool(Pool):
    def __init__(self, origin: asyncpg.pool.Pool):
        self._origin = origin
    
    def acquire(self, timeout: float) -> PoolAcquireContext:
        origin_context = self._origin.acquire(timeout=timeout)
        context = AsyncpgPoolAcquireContext(origin=origin_context)
        return context
    
    async def close(self) -> None:
        await self._origin.close()


class AsyncpgFactory():
    async def create_pool(
        self,
        dsn: str,
        min_size: int = 10,
        max_size: int = 10,
    ) -> Pool:
        try:
            origin: asyncpg.pool.Pool = await asyncpg.create_pool(
                dsn,
                max_size=max_size,
                min_size=min_size,
            )
        except asyncpg.exceptions.InterfaceError:
            raise PoolConnectionError('Failed to connect pool.')
        pool = AsyncpgPool(origin=origin)
        return pool
