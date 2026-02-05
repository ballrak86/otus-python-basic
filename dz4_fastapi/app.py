import uvicorn
from fastapi import FastAPI
from routers.main_router import main_router
from routers.api_router import api_router

app = FastAPI()

app.include_router(main_router, tags=["main_router"])
app.include_router(api_router, tags=["api_router"], prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
