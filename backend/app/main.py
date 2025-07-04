import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routers.products import router as products_router
from app.api.routers.users import router as users_router
from app.config import settings
from app.database import sessionmanager
from app.services.elasticsearch import ensure_index
from app.web.routers.home import router as home_router

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.log_level == "DEBUG" else logging.INFO)
logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    logger.info("ensuring Elasticsearch index exists...")
    ensure_index()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# Routers
app.include_router(users_router)
app.include_router(home_router)
app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
