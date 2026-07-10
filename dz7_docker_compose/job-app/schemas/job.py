from datetime import date
from pydantic import BaseModel, ConfigDict


class JobBaseSchema(BaseModel):
    title: str
    description: str | None
    due_date: date
    completed: bool = False


class JobReadSchema(JobBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
