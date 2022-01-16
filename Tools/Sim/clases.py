from typing import List
from enum import Enum

import random
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
        self.windResistence = 20
        self.speed = 0

class Satellite:
    def __init__(self, usefulLife: int):
        self.usefulLife = usefulLife

class Junk:

    def __init__(self, size: float, position):
        self.size = size
        self.position =position

    def __str__(self) -> str:
        return f"size:{self.size}-position:{self.position}"

def generateJunk():
    junks = []
    for _ in range(1, random.randint(5, 100)):
        x,y,z = random.randint(1,100),random.randint(1,100),random.randint(1,100)
        junks.append(Junk(random.randint(1,10),(x,y,z)))
    return junks

for junk in generateJunk():
    print(junk)
    
class EnvironmentMap:

    def __init__(self, maxX, maxY, maxZ):
        ...

