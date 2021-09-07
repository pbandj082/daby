import asyncpg

from .connection import AsyncpgConnection
from ...pool import PoolAcquireContext, Pool
from ...exceptions import PoolConnectionError


@PoolAcquireContext.register
class AsyncpgPoolAcquireContext():
    def __init__(self, origin: asyncpg.pool.PoolAcquireContext):
        self._origin = origin
    
    async def __aenter__(self) -> AsyncpgConnection:
        origin_connection = await self._origin.__aenter__()
        connection = AsyncpgConnection(origin=origin_connection)
        return connection


    async def __aexit__(self) -> None:
        await self._origin.__aexit__()


@Pool.register
class AsyncpgPool:
    def __init__(self, origin: asyncpg.pool.Pool):
        self._origin = origin
    
    def acquire(self, timeout: float) -> PoolAcquireContext:
        origin_context = self._origin.acquire(timeout=timeout)
        context = AsyncpgPoolAcquireContext(origin=origin_context)
        return context
    
    async def close(self) -> None:
        await self._origin.close()


async def create_asyncpg_pool(
    dsn: str,
    min_size: int = 10,
    max_size: int = 10,
) -> AsyncpgPool:
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
