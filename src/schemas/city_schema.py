from pydantic import BaseModel, Field
from datetime import datetime


class CityInformation(BaseModel):
    city_id: int
    temperature: float
    humidity: float


class CitySchema(BaseModel):

    time: datetime = datetime.now()
    information: CityInformation


class CityOutputSchema(BaseModel):

    time: datetime
    information: CityInformation
