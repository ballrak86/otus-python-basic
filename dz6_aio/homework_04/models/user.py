from typing import TYPE_CHECKING

from sqlalchemy import (
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .mixins import IdIntPKMixin

if TYPE_CHECKING:
    from .post import Post


class User(IdIntPKMixin, Base):
    name: Mapped[str] = mapped_column(
        Text,
        unique=False,
    )

    username: Mapped[str] = mapped_column(
        Text,
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        Text,
        unique=True,
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )
