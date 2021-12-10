from typing import List

from enum import Enum


class RocketStatus(Enum):
   
    GOOD = 0
    BAD = 1
    REGULAR = 2
    

class Rocket:


    def __init__(self, weight: float, fuel:int , satellites: List['Satellite'] = []) -> None:
        self.weight = weight
        self.fuel = fuel
        self.satellites = satellites
        self.status = RocketStatus.GOOD
        self.life = 100

    

class Satellite:

    def __init__(self, usefulLife: int):
        self.usefulLife = usefulLife

class Junk:

    def __init__(self, size: float):
        self.size = size

    