
import random
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