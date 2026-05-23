import asyncio
from typing import Any

import aiohttp

from .jsonplaceholder_requests import *


async def fetch(url: str) -> list[dict[str, Any]]:
    """отправить один запрос на API и отдать результат"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def concurrent_fetch():
    """конкурентно получить данные о пользователях и постах"""
    users_data, posts_data = await asyncio.gather(
        fetch(USERS_DATA_URL),
        fetch(POSTS_DATA_URL),
    )
    return users_data, posts_data
