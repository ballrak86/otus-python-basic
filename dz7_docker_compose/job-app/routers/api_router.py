from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse

from schemas.job import JobReadSchema
from routers.auth import get_session_username


from models.db import session_factory
from .crud import JobCRUD

import asyncio
from typing import Any

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@api_router.get("/", response_class=HTMLResponse)
async def api_list(
    request: Request,
    user_session_data: dict = Depends(get_session_username),
):
    """Список всех задач"""
    with session_factory() as session:
        crud = JobCRUD(session)
        to_do_list = crud.get_list()
    context = {
        "request": request,
        "title": "Список задач",
        "text": "Здесь созданные тобой задачи",
        "to_do_list": to_do_list,
        "user_name": user_session_data["username"],
    }
    return templates.TemplateResponse(
        name="index.html", context=context, request=request
    )


async def event_generator():
    """Генератор для sse"""
    count = 0
    while True:
        await asyncio.sleep(1)
        with session_factory() as session:
            crud = JobCRUD(session)
            to_do_list = crud.get_list()
        len_to_do_list = len(to_do_list)
        string = ""
        for num, i in enumerate(to_do_list):
            if i.completed:
                checked = "checked"
            else:
                checked = ""
            string += f'<div class="col">  <div class="card mb-4 rounded-3 shadow-sm">  <div class="card-header py-3">  <h4 class="my-0 fw-normal"><a href="/api/item/{i.id}">{i.title}</a></h4>  </div>  <div class="card-body">  <h1 class="card-title pricing-card-title">{i.due_date}<small class="text-muted fw-light"></small></h1>  <ul class="list-unstyled mt-3 mb-4">  <li>{i.description}</li>  </ul>  <div class="form-check form-switch">  <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" {checked}>  <label class="form-check-label" for="flexSwitchCheckDefault">Default switch checkbox input</label>  </div>  </div>  </div>  </div>'
            if num >= len_to_do_list:
                string += "\n\n"
        count += 1
        yield f"data: {count} {string}\n\n"


@api_router.get("/sse")
async def sse():
    """Server-sent event"""
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@api_router.get("/item/{id_item}", response_class=HTMLResponse)
async def read_item(
    request: Request,
    id_item: int,
    user_session_data: dict = Depends(get_session_username),
):
    """Посмотреть определенную задачу"""
    with session_factory() as session:
        crud = JobCRUD(session)
        item = crud.get_by_id(id_item)
    context = {
        "request": request,
        "title": "Редактирование задачи",
        "text": "Введите новые значения для полей",
        "to_do_list": item,
        "user_name": user_session_data["username"],
    }
    return templates.TemplateResponse(
        request=request, name="item.html", context=context
    )


@api_router.get("/new", response_class=HTMLResponse)
async def input_item(
    request: Request, user_session_data: dict = Depends(get_session_username)
):
    """Форма заполнения данных для новой задачи"""
    context = {
        "request": request,
        "title": "Создание задачи",
        "text": "Введите значения для полей",
        "user_name": user_session_data["username"],
    }
    return templates.TemplateResponse(
        request=request, name="new_item.html", context=context
    )


@api_router.post("/job_create", response_model=JobReadSchema, status_code=201)
async def job_create(
    title=Form(default=None),
    description=Form(default=None),
    due_date=Form(default=None),
    completed: bool = Form(default=False),
):
    """Добавить новую задачу"""
    if not (title and description and due_date):
        raise HTTPException(status_code=400, detail="write all fields")
    job = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": completed,
    }
    with session_factory() as session:
        crud = JobCRUD(session)
        item = crud.create(job)
        job["id"] = item.id
    return job


@api_router.post("/{id_item}", response_model=JobReadSchema)
async def job_update(
    id_item: int,
    title=Form(default=None),
    description=Form(default=None),
    due_date=Form(default=None),
    completed: bool = Form(default=False),
):
    """Обновить задачу"""
    job = {
        "id": id_item,
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": completed,
    }
    with session_factory() as session:
        crud = JobCRUD(session)
        item = crud.update(job)
    return item
