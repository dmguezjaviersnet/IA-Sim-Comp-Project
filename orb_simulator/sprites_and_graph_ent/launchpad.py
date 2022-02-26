from dataclasses import dataclass
from simulation.generate_objects import generate_waiting_time

class Launchpad:

    def __init__(self, time_of_occurrence):
        self.lauch_that_is_running = None
        self.rocket_in_queue = []
        self.time_of_occurrence = time_of_occurrence
        self.next_arrival_time = generate_waiting_time()
        self.next_departure_time = None


    @property
    def number_of_rocket_in_system(self):
        l = len(self.rocket_in_queue)
        if self.lauch_that_is_running:
            l +=1
        return l
    
    def generate_next_arrival(self, current_time: float):
        self.next_arrival_time = generate_waiting_time() +  current_time
    
    def generate_next_departure(self, current_time: float):
        self.next_departure_time = generate_waiting_time() +current_time
