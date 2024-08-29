import logging
from asyncio import run

from tortoise.backends.asyncpg import AsyncpgDBClient
from tortoise_api_model import init_db
from xync_schema import models

from xync_scripts.loader import dsn

logging.basicConfig(level=logging.DEBUG)


def test_init_db():
    cn = run(init_db(dsn, models))
    assert isinstance(cn, AsyncpgDBClient), "DB corrupt"
