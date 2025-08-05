# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os

from api.db import init_db
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    init_db()
    yield
    # after app startup

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats")

API_KEY = os.environ.get("API_KEY")
MY_PROJECT = os.environ.get("PROJECT_NAME")

if not API_KEY:
    raise NotImplementedError("'API_KEY' was not set")

@app.get("/")
def read_index():
    return {"hello":"world again!", "project_name":MY_PROJECT}

@app.get("/health")
def read_index():
    return {"status":"ok!"}