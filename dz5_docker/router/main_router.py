from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get('/')
async def index():
    """Редирект на нужный нам путь"""
    return RedirectResponse(url='/ping')


@router.get('/ping/', status_code=200)
async def view():
    """отвечаем pong в json"""
    return {"message": "pong"}
