from typing import TYPE_CHECKING

from sqlalchemy import (
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .mixins import IdIntPKMixin

if TYPE_CHECKING:
    from .user import User


class Post(IdIntPKMixin, Base):

    title: Mapped[str] = mapped_column(
        Text,
        unique=False,
        default="",
        server_default="",
    )

    body: Mapped[str] = mapped_column(
        Text,
        unique=False,
        default="",
        server_default="",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="posts",
    )
