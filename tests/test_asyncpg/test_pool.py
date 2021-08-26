import pytest

from daby import AsyncpgFactory


@pytest.mark.asyncio
async def test_create_pool(database_url: str):
    factory = AsyncpgFactory()
    pool = await factory.create_pool(database_url)
    await pool.close()

