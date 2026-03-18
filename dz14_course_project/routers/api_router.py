from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from schemas.jobs import Job
from routers.auth import get_session_username

import asyncio
from typing import Any

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")

to_do_list = [
    Job(
        job_id=1,
        title='Первая задача',
        description='Описание задачи',
        due_date='2026-02-05',
        completed=False
    ),
    Job(
        job_id=2,
        title='Вторая задача',
        description='Другое описание',
        due_date='2026-02-01',
        completed=True
    ),
    Job(
        job_id=3,
        title='Третья задача',
        description='Еще одно описание',
        due_date='2026-02-02',
        completed=False
    ),
]


@api_router.get('/', response_class=HTMLResponse)
async def api_list(request: Request, user_session_data: dict = Depends(get_session_username)):
    """Список всех задач"""
    context = {
        'request': request,
        'title': 'Список задач',
        'text': 'Здесь созданные тобой задачи',
        'to_do_list': to_do_list,
        'user_name': user_session_data['username'],
    }
    return templates.TemplateResponse('index.html', {"request": request})


async def event_generator():
    """Генератор для sse"""
    count = 0
    while True:
        await asyncio.sleep(1)
        len_to_do_list = len(to_do_list)
        string = ''
        for num, i in enumerate(to_do_list):
            if i.completed:
                checked = 'checked'
            else:
                checked = ''
            string += f'<div class="col">  <div class="card mb-4 rounded-3 shadow-sm">  <div class="card-header py-3">  <h4 class="my-0 fw-normal"><a href="/api/item/{i.job_id}">{i.title}</a></h4>  </div>  <div class="card-body">  <h1 class="card-title pricing-card-title">{i.due_date}<small class="text-muted fw-light"></small></h1>  <ul class="list-unstyled mt-3 mb-4">  <li>{i.description}</li>  </ul>  <div class="form-check form-switch">  <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" {checked}>  <label class="form-check-label" for="flexSwitchCheckDefault">Default switch checkbox input</label>  </div>  </div>  </div>  </div>'
            if num >= len_to_do_list:
                string += '\n\n'
        count += 1
        yield f"data: {count} {string}\n\n"


@api_router.get("/sse")
async def sse():
    """Server-sent event"""
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@api_router.get("/item/{id_item}", response_class=HTMLResponse)
async def read_item(request: Request, id_item: int, user_session_data: dict = Depends(get_session_username)):
    """Посмотреть определенную задачу"""
    context = {}
    for item in to_do_list:
        if item.job_id == id_item:
            context = {
                'request': request,
                'title': 'Редактирование задачи',
                'text': 'Введите новые значения для полей',
                'to_do_list': item,
                'user_name': user_session_data['username'],
            }
    print(context)
    return templates.TemplateResponse(request=request, name="item.html", context=context)


@api_router.get("/new", response_class=HTMLResponse)
async def input_item(request: Request, user_session_data: dict = Depends(get_session_username)):
    """Форма заполнения данных для новой задачи"""
    context = {
        'request': request,
        'title': 'Создание задачи',
        'text': 'Введите значения для полей',
        'user_name': user_session_data['username'],
    }
    return templates.TemplateResponse(request=request, name="new_item.html", context=context)


@api_router.post("/job_create", response_model=Job, status_code=201)
async def job_create(title=Form(default=None), description=Form(default=None), due_date=Form(default=None),
                     completed: bool = Form(default=False)):
    """Добавить новую задачу"""
    if not (title and description and due_date):
        raise HTTPException(status_code=400, detail='write all fields')
    lst = []
    for item in to_do_list:
        lst.append(item.job_id)
    job_id = (max(lst) + 1)
    job = Job(job_id=job_id, title=title, description=description, due_date=due_date, completed=completed)
    to_do_list.append(job)
    return job


@api_router.post("/{id_item}", response_model=Job)
async def job_update(id_item: int, title=Form(default=None), description=Form(default=None),
                     due_date=Form(default=None), completed: bool = Form(default=False)):
    """Обновить задачу"""
    if id_item < 0 or id_item > len(to_do_list):
        raise HTTPException(status_code=404, detail='job not found')
    num = 0
    for num, item in enumerate(to_do_list, start=0):
        if item.job_id == id_item:
            to_do_list[num].title = title if title else to_do_list[num].title
            to_do_list[num].description = description if description else to_do_list[num].description
            to_do_list[num].due_date = due_date if due_date else to_do_list[num].due_date
            to_do_list[num].completed = completed
            break
    return to_do_list[num]
