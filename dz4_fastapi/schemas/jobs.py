from pydantic import BaseModel


class Job(BaseModel):
    job_id: int
    title: str
    description: str
    due_date: str
    completed: bool
