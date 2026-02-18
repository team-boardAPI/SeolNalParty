from fastapi import FastAPI

import app.models.comment  # noqa: F401
import app.models.post  # noqa: F401
import app.models.user  # noqa: F401
from app.core.database import Base, engine
from app.routers.auth import auth_router
from app.routers.comments import router as comments_router
from app.routers.users import users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Board Service", description="Board Api", version="1.0.0")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(comments_router)


@app.get("/")
def test():
    return {"Hello": "World"}
