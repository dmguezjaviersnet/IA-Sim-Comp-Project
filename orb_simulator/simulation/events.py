
from dataclasses import dataclass
import random
import math
from typing import List
import numpy as np
@dataclass
class CreateSpaceDebrisEvent:
    name: str
    ocurrence_time : float


class HomogeneousPoissonProcess:
    '''
        Proceso de Poisson homogéneo para generar nuevos pedazos de basura spacial
    '''
    def __init__(self, T, lambda_value):
        self.closing_time = T
        self.events_ocurred:List['CreateSpaceDebrisEvent'] = []
        self.lambda_value = lambda_value
        self.compute_next_event_time(0)
        

    @property
    def number_of_events_ocurred(self):
        return len(self.events_ocurred)
    
    def compute_next_event_time(self, t: float):
        random_uniform = random.random()
        next_t = t - (1/self.lambda_value)*math.log(random_uniform)
        self.next_event_time = next_t

    
    def generate_next_event(self):
        new_event = CreateSpaceDebrisEvent(f'Event{self.number_of_events_ocurred +1}', self.next_event_time)
        print(f'Event{self.number_of_events_ocurred +1} {self.next_event_time}')
        self.events_ocurred.append(new_event)
        self.compute_next_event_time(self.next_event_time)


