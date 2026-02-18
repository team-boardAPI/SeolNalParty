from fastapi import FastAPI, APIRouter
from app.routers import comments


app = FastAPI()
router = APIRouter()

app.include_router(comments.router)




