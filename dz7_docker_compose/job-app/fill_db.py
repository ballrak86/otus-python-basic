from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from models import Job, Base
from models.db import engine


def insert_values() -> None:
    job_1 = Job(
        title="Первая задача",
        description="Описание задачи",
        due_date="2026-08-05",
        completed=False,
    )
    job_2 = Job(
        title="Вторая задача",
        description="Другое описание",
        due_date="2026-08-01",
        completed=True,
    )
    job_3 = Job(
        title="Третья задача",
        description="Еще одно описание",
        due_date="2026-08-02",
        completed=False,
    )
    with Session(engine) as session:
        session.add_all([job_1, job_2, job_3])
        session.commit()


def main():
    with Session(engine) as session:
        if not database_exists(engine.url):
            create_database(engine.url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    insert_values()


main()
