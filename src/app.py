from fastapi import FastAPI
from concurrent.futures.process import ProcessPoolExecutor
from routers.devgrid_router import dev_router
from core.db import engine, Base
from loguru import logger
from models.city_model import City


app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        logger.info("Tables created")
        await conn.run_sync(Base.metadata.create_all)


app.include_router(dev_router, tags=['TEST'])
