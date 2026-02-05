from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas.jobs import Job

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
async def api_list(request: Request):
    """Список всех задач"""
    context = {
        'request': request,
        'title': 'Список задач',
        'text': 'Здесь созданные тобой задачи',
        'to_do_list': to_do_list,
    }
    return templates.TemplateResponse('index.html', context=context)


@api_router.get("/item/{id_item}", response_class=HTMLResponse)
async def read_item(request: Request, id_item: int):
    """Посмотреть определенную задачу"""
    context = {}
    for item in to_do_list:
        if item.job_id == id_item:
            context = {
                'request': request,
                'title': 'Редактирование задачи',
                'text': 'Введите новые значения для полей',
                'to_do_list': item,
            }
    return templates.TemplateResponse(request=request, name="item.html", context=context)


@api_router.get("/new", response_class=HTMLResponse)
async def input_item(request: Request):
    """Форма заполнения данных для новой задачи"""
    context = {
        'request': request,
        'title': 'Создание задачи',
        'text': 'Введите значения для полей',
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
    if id_item < 0 or id_item >= len(to_do_list):
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
