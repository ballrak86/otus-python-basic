from datetime import date

from sqlalchemy import (
    Text,
    func,
    Boolean,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from .mixins import IdIntPKMixin

from .base import Base


class Job(Base, IdIntPKMixin):
    title: Mapped[str] = mapped_column(
        Text,
    )

    description: Mapped[str] = mapped_column(
        Text,
        server_default="",
    )

    due_date: Mapped[date] = mapped_column(
        server_default=func.now(),
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        # server_default=func.false(),
    )

    def __repr__(self):
        dct = {
            "job_id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
        }
        return f"Job(job_id:'{self.id}', title: '{self.title}', description: '{self.description}', due_date: '{self.due_date}', completed: {self.completed}))"
