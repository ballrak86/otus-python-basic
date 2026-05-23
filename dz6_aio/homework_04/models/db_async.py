from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import homework_04.config

async_engine = create_async_engine(
    url=homework_04.config.SQLA_ASYNC_URL,
    echo=homework_04.config.SQLA_ECHO,
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
