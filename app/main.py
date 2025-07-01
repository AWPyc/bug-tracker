from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.db.init_db import init_db
from app.routers import bug_router, tag_router

import logging
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(bug_router.router)
app.include_router(tag_router.router)

@app.get("/")
def root():
    return {"message": "Bug tracker API is running"}

