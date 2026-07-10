from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers.auth import get_session_username

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@main_router.get('/', response_class=HTMLResponse)
async def index(request: Request, user_session_data: dict = Depends(get_session_username)):
    """"""
    context = {
        'request': request,
        'title': 'ToDoList',
        'text': 'Здесь вы сможете создать свои задачи',
        'user_name': user_session_data['username'],
    }
    return templates.TemplateResponse(name='about.html', context=context, request=request)


@main_router.get('/about/', response_class=HTMLResponse)
async def about(request: Request, user_session_data: dict = Depends(get_session_username)):
    context = {
        'request': request,
        'title': 'Контакты',
        'text': 'Разработчик на Python',
        'first_last_name': 'Ленчик Алексей Алексеевич',
        'user_name': user_session_data['username'],
    }
    return templates.TemplateResponse(name='about.html', context=context, request=request)
