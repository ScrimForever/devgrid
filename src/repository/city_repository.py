import datetime
from dataclasses import dataclass
from models.city_model import City
from sqlalchemy import insert
from core.db import engine
from loguru import logger


@dataclass
class CityRepository:

    @staticmethod
    async def persist_data(request_id, data):
        query = insert(City).returning(City).values(
            request_id=request_id,
            time=datetime.datetime.now(),
            information={
                "city_id":data.get("id"),
                "temperature": data.get("main").get("temp"),
                "humidity": data.get("main").get("humidity")
            })
        try:
            async with engine.begin() as conn:
                await conn.execute(query)
                await conn.commit()
                return True
        except Exception as e:
            logger.error(e)
            return False
