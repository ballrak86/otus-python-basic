from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@main_router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    context = {
        'request': request,
        'title': 'ToDoList',
        'text': 'Здесь вы сможете создать свои задачи',
    }
    return templates.TemplateResponse('about.html', context=context)


@main_router.get('/about/', response_class=HTMLResponse)
async def about(request: Request):
    context = {
        'request': request,
        'title': 'Контакты',
        'text': 'Разработчик на Python',
        'first_last_name': 'Ленчик Алексей Алексеевич',
    }
    return templates.TemplateResponse('about.html', context=context)
