from fastapi import FastAPI

import app.models.user as user
from app.core.database import engine
from app.routers.auth import auth_router
from app.routers.users import users_router

user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Board Service", description="Board Api", version="1.0.0")

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def test():
    return {"Hello": "World"}
