import asyncpg

from ...connection import Connection


@Connection.register
class AsyncpgConnection():
    def __init__(self, origin: asyncpg.Connection):
        self._origin = origin
