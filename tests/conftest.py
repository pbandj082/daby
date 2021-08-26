import asyncio
import pytest
from dotenv import load_dotenv
import os


@pytest.fixture(scope='session')
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope='session')
def database_url() -> str:
    load_dotenv()
    return os.getenv('DATABASE_URL')
