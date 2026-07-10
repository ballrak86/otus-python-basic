from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    url=settings.db.url,
    echo=settings.db.sqla.echo,
)

session_factory = sessionmaker(
    bind=engine,
)
