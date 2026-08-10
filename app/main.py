from typing import Callable

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import category, task
from app.core.config import get_settings
from app.models import category as category_model  # noqa: F401
from app.models import task as task_model  # noqa: F401

settings = get_settings()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
middleware_count = 0


@app.middleware("http")
async def middleware(request: Request, call_next: Callable):
    global middleware_count
    middleware_count += 1
    response = await call_next(request)
    response.headers["X-request-number"] = str(middleware_count)
    return response


app.include_router(task.router)
app.include_router(category.router)
