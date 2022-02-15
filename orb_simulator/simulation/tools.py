from dataclasses import dataclass
import random
import math
from typing import List

@dataclass
class Event:
    name: str
    ocurrence_time : int

    
# evento de Poisson homogéneos para simular  la ocurrencia de eventos discretos
def poisson_process(T, plambda = 0.0025):
    t = 0
    l:List[Event] = []
    while t <= T:
        rand1 = random.random()
        t = t - (1/plambda)*math.log(rand1)
        # rand2 = random.random()
        new_event = Event(f'evento{len(l)+1}',t);
        print(new_event)
        l.append(new_event)

    return l

poisson_process(1000)