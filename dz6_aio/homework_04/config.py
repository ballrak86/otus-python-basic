from os import getenv
from sqlalchemy import URL

PG_HOST = "localhost"
PG_PORT = 5432
# PG_DB = "blog"
PG_USER = "postgres"
PG_PASSWORD = "password"

SQLA_ASYNC_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT,
    #    database=PG_DB,
)
print(SQLA_ASYNC_URL.render_as_string(hide_password=False))

SQLA_ECHO = True
if getenv("SQLALCHEMY_ECHO"):
    SQLA_ECHO = True
