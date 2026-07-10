import secrets
import uuid
from typing import Annotated, Any
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()

security = HTTPBasic()

usernames_to_passwords = {
    "admin": "admin",
}


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    """проверка логина и пароля пользователя"""
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    # secrets
    if not secrets.compare_digest(
            credentials.password.encode("utf-8"),
            correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
        response: Response, auth_username: str = Depends(get_auth_user_username),
):
    """Авторизация через cookie с использованием Basic auth"""

    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def get_session_username(session_id: str | None = Cookie(alias=COOKIE_SESSION_ID_KEY, default=None)):
    """Получение имени пользователя по id сессии"""
    if session_id == None:
        return {'username': ''}
    return COOKIES[session_id]


def generate_session_id() -> str:
    """Генерация id сессии"""
    return uuid.uuid4().hex


@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
        response: Response,
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
        user_session_data: dict = Depends(get_session_username),
):
    """Выход из системы и удаление cookies"""
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    response.delete_cookie("Authorization")
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}!",
    }
