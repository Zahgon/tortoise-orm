from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from config import register_orm
from fastapi import FastAPI
from routers import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    pass


app = FastAPI(title="Tortoise ORM FastAPI example", lifespan=lifespan)
app.include_router(users_router, prefix="")
