"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio

from sqlalchemy.orm import Session

from homework_04.fetch_api import concurrent_fetch
from homework_04.models.base import Base
from homework_04.models.user import User
from homework_04.models.post import Post
from homework_04.models.db_async import async_engine, async_session


async def initial_creation(session: Session, users_data, posts_data):
    """Заполняем БД"""
    for user in users_data:
        name = user.get("name")
        username = user.get("username")
        email = user.get("email")
        session.add(User(name=name, username=username, email=email))
        await session.flush()
    for post in posts_data:
        user_id = post.get("userId")
        title = post.get("title")
        body = post.get("body")
        session.add(Post(user_id=user_id, title=title, body=body))


async def async_main():
    """Асинхронная функция"""
    print(Base.metadata.tables)
    async with async_engine.connect() as conn, conn.begin():
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    users_data, posts_data = await concurrent_fetch()
    async with async_session() as session, session.begin():
        await initial_creation(session, users_data, posts_data)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
