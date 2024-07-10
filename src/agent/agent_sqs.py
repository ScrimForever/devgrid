import os
import time
from loguru import logger
from services.weather_services_api import WeatherServices
from helpers.config import receive_client
from repository.city_repository import CityRepository
from repository.request_repository import RequestRepository
import json
from redis import Redis


async def loop_message():
    r = Redis(host='cache', port=6379, db=0, decode_responses=True)
    count = 0
    while True:
        try:
            messages = receive_client.receive_message(
                QueueUrl=f'{os.getenv("SQS_URL")}',
                MaxNumberOfMessages=10,
                VisibilityTimeout=0,
                WaitTimeSeconds=0
            )

            if count == 60:
                logger.debug('60 messages received')
                time.sleep(60)
                count = 0

            for i in messages['Messages']:


                try:
                    json_body = json.loads(i['Body'])
                    _request_id = json_body.get('request_id')
                    logger.debug(json_body)
                    weather_city = await WeatherServices(city_id=json_body.get('city_id')).get_weather_data()
                    if weather_city:
                        logger.debug(weather_city)
                        response_created = await CityRepository().persist_data(
                            request_id=json_body.get('request_id'),
                            data=weather_city
                        )
                        try:
                            total_processed = r.get(f'{_request_id}')
                            if total_processed is None:
                                r.set(f'{_request_id}', '1')
                            else:
                                total = int(total_processed) + 1
                                r.set(f'{_request_id}', str(total))
                        except Exception as e:
                            logger.error(e)
                        logger.debug('persisted')
                        if response_created:
                            receive_client.delete_message(
                                QueueUrl=f'{os.getenv("SQS_URL")}',
                                ReceiptHandle=i['ReceiptHandle']
                            )
                except Exception as e:
                    logger.error(e)
            _keys = r.keys('*')
            for k in _keys:
                _value = int(r.get(k))
                _persist_request = await RequestRepository().update_data(request_id=k, total_processed=_value)
                if _persist_request:
                    logger.debug(f'{_persist_request}')
            count = count + 10
        except KeyError as e:
            logger.warning(f'No: {e}')
            time.sleep(60)