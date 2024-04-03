from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from src.pages.router import router as pages_router

app = FastAPI(
    title="Lesta Games test task"
)


templates = Jinja2Templates(directory="src/templates")
app.include_router(pages_router)





