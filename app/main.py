from contextlib import asynccontextmanager

from db.db import create_all_tables
from fastapi import FastAPI
from routers import auth_router, profile_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI project!"}


app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(profile_router.router)
