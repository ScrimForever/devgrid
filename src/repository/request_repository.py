import datetime
from dataclasses import dataclass
from models.request_model import RequestModel
from sqlalchemy import insert, select, update
from core.db import engine
from loguru import logger


@dataclass
class RequestRepository:

    @staticmethod
    async def persist_data(request_id, size):
        query = insert(RequestModel).returning(RequestModel).values(
            request_id=request_id,
            total_cities=size,
            processed_city=0,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        try:
            async with engine.begin() as conn:
                await conn.execute(query)
                await conn.commit()
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def update_data(request_id, total_processed):
        query = update(RequestModel).where(RequestModel.request_id == request_id).values(
            processed_city=total_processed,
            updated_at=datetime.datetime.now(),
        )
        logger.debug(f'QUERY: {query}')
        try:
            async with engine.begin() as conn:
                await conn.execute(query)
                await conn.commit()
                return True
        except Exception as e:
            logger.error(e)
            return False

    async def get_request(self, request_id, session):
        query = select(RequestModel).where(RequestModel.request_id == request_id)
        executed = await session.execute(query)
        return executed.scalar()