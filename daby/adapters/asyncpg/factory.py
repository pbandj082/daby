from .pool import create_asyncpg_pool
from ...pool import Pool


class AsyncpgFactory():
    async def create_pool(
        self,
        dsn: str,
        min_size: int = 10,
        max_size: int = 10,
    ) -> Pool:
        pool = await create_asyncpg_pool(
            dsn,
            min_size=min_size,
            max_size=max_size,
        )
        return pool
