import os
from dataclasses import dataclass


@dataclass
class Config:

    OPENKEY = os.getenv('OPENKEY')
