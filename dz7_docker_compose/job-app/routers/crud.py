from sqlalchemy import select, update
from sqlalchemy.orm import Session
from models import Job


class JobCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self) -> list[Job]:
        statement = select(Job).order_by(Job.id)
        result = self.session.scalars(statement)
        return list(result.all())

    def get_by_id(self, job_id: int) -> Job | None:
        return self.session.get(Job, job_id)

    def create(self, job_dict: dict) -> Job:
        job = Job(**job_dict)
        self.session.add(job)
        self.session.commit()
        return job

    def update(self, job_dict: dict) -> Job | None:
        job = self.get_by_id(job_dict["id"])
        if job:
            for key, value in job_dict.items():
                if value:
                    setattr(job, key, value)
        self.session.commit()
        job = self.get_by_id(job_dict["id"])
        return job
