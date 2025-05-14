from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from db.db import create_all_tables
from contextlib import asynccontextmanager
from model.user import User
from routers import user_router, auth_router, profile_router

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