from fastapi import FastAPI

from app.routers import tasks


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(tasks.router)

    return app
