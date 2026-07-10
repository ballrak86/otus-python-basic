from sqlalchemy import (
    Identity,
    BigInteger,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class IdIntPKMixin(object):
    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
