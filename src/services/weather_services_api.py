from dataclasses import dataclass
from config.config import Config
from http import HTTPStatus
import httpx
from loguru import logger


@dataclass
class WeatherServices:

    def __init__(self, city_id):
        self.key = Config.OPENKEY
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather?id='
        self.city_id = city_id

    async def _make_request(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.base_url}{self.city_id}&units=metric&appid={self.key}')
            if response.status_code == HTTPStatus.OK:
                resp_json = response.json()
                logger.info(f"City {self.city_id} retrieved")
                return resp_json
            else:
                return False

    async def get_weather_data(self):
        resp_json = await self._make_request()
        return resp_json
