from dataclasses import dataclass
from loguru import logger
from typing import Dict
from schemas.city_schema import CitySchema, CityInformation
from datetime import datetime
from repository.city_repository import CityRepository
from services.weather_services_api import WeatherServices


@dataclass
class CityHandler:

    def __init__(self, code, session):
        self.code = code
        self.session = session

    @staticmethod
    async def _get_city(city_id):
        try:
            logger.info(f"Getting city {city_id}")
            weather_services = await WeatherServices(city_id=city_id).get_weather_data()
            return weather_services
        except Exception as e:
            logger.error(e)
            return False

    async def _treatment(self, data: Dict):

        weather_information = CityInformation(city_id=self.code,
                                              temperature=data['main']['temp'],
                                              humidity=data['main']['humidity'])
        weather_object = CitySchema(time=datetime.now(), information=weather_information)
        return weather_object

    async def _get_city_data_from_api(self, city_id):

        response_data_geocode = await self._get_city(city_id)
        logger.info(response_data_geocode)

        logger.info('*' * 80)
        
        treatment_response = await self._treatment(response_data_geocode)
        logger.info(treatment_response)

        persisted = await self._persist_data_on_database(treatment_response)
        return persisted

    async def _persist_data_on_database(self, data: CitySchema):
        city = await CityRepository(session=self.session).persist_data(data)
        return city

    async def make_request(self):
        return await self._get_city_data_from_api(self.code)
