
from dataclasses import dataclass
import random
import math
from typing import List
import numpy as np
@dataclass
class Event:
    name: str
    ocurrence_time : int

    
# evento de Poisson homogéneos para simular  la ocurrencia de eventos discretos
def poisson_process_homogeneous(T, plambda = 0.0025):
    t = 0
    l:List[Event] = []
    while t <= T:
        rand1 = random.random()
        t = t - (1/plambda)*math.log(rand1)
        # rand2 = random.random()
        new_event = Event(f'evento{len(l)+1}',t)
        print(new_event)
        l.append(new_event)
    
    return l

def poisson_process_nothomogeneous(T):
    t = 0
    l:List[Event] = []
    values = np.arange((T * 0.9) * 5, dtype=float) / 5
    plambda = max([intensity_function(t) for t in values])
    print(plambda)
    while t <= T:
        rand1 = random.random()
        t = t - (1/plambda)*math.log(rand1)
        rand2 = random.random()
        if rand2 <=intensity_function(t)/plambda:
            new_event = Event(f'evento{len(l)+1}',t);
            print(new_event)
            l.append(new_event)
    
    return l

def intensity_function(t):
    return 1 / 100*(math.sin(t*math.pi)) +1 

poisson_process_nothomogeneous(100)