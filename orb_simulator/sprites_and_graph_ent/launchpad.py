from dataclasses import dataclass
from typing import List
from click import launch

from urllib3 import Retry
from simulation.generate_objects import generate_waiting_time, generate_new_rocket
from sprites_and_graph_ent.rocket import Rocket
from tools import round_off_wi_exceed
from sprites_and_graph_ent.eliptic_orbit import ElipticOrbit

class RocketForm:
    def __init__(self, arrival_time):
        self.id = id(self)
        self.arrival_manufacturing = arrival_time
        self.arrival_launchpad = None
        self.departure_time_manufacturing = None
        self.departure_time_launchpad = None
        self.rocket: Rocket = None
    
    def __str__(self):
        return f'Rocket_{self.id} \n Time_arrival_manufacturing = {self.arrival_manufacturing} \n Time_arrival_launchpad = {self.departure_time_launchpad}\n Time_departure_manufacturing = {self.departure_time_manufacturing} \n Time_departure_launchpad = {self.departure_time_manufacturing}'
    def set_arrival_launchpad(self, time):
        self.arrival_launchpad = time
    
    def set_departure_time_manufacturing(self, time):
        self.departure_time_manufacturing = time

    def set_departure_time_launchpad(self, time):
        self.departure_time_launchpad = time



class Launchpad:

    def __init__(self, closing_time, lambda_value):
        self.lauch_that_is_running = None
        self.rocket_in_queue = []
        self.closing_time = closing_time
        self.lambda_value = lambda_value
        self.rocket_manufacturing = RocketManufacturing(lambda_value, closing_time)
        self.next_departure_time = None
        self.number_of_arrivals = 0
        self.number_of_departure = 0
        self.forms: List['RocketForm'] = []
        
    @property
    def any_enqueue_action(self):
        return self.lauch_that_is_running or self.rocket_manufacturing.rocket_being_manufactured

    @property 
    def next_arrival_to_manufacturing(self):
        return self.rocket_manufacturing.next_arrival_time

    @property
    def next_manufacturing_departure(self):
        return self.rocket_manufacturing.next_departure_time

    @property
    def is_any_rocket_manufacturing(self):
        return self.rocket_manufacturing.rocket_being_manufactured != None
    @property
    def number_of_rockets(self):
        l = len(self.rocket_in_queue)
        if self.lauch_that_is_running:
            l +=1
        return l
    
    def generate_next_arrival(self, current_time: float):
        self.next_arrival_time = generate_waiting_time(self.lambda_value) +  current_time
    
    def generate_next_departure_launchpad(self, current_time: float):
        self.next_departure_time = generate_waiting_time(self.lambda_value) + current_time

    def generate_next_departure_manufacturing(self, current_time: float):
        self.rocket_manufacturing.generate_next_departure(current_time)
    
    def update(self, current_time: float, orbits: List['ElipticOrbit']):
        rounded_current_time = round_off_wi_exceed(current_time)
        
        if round_off_wi_exceed(self.next_arrival_to_manufacturing) == rounded_current_time:
           self.rocket_manufacturing.add_rocket_form(current_time)
        print(self.is_any_rocket_manufacturing)
        if  self.is_any_rocket_manufacturing  and round_off_wi_exceed(self.next_manufacturing_departure) == rounded_current_time:
            rocket_form = self.rocket_manufacturing.rocket_being_manufactured
            new_rocket = generate_new_rocket(orbits)
            rocket_form.set_arrival_launchpad(current_time)
            rocket_form.rocket = new_rocket
            self.rocket_manufacturing.update_departure(current_time)
            self.add_rocket_form(rocket_form, current_time)
            self.next_arrival_time = current_time
        
    
    def update_out_of_time(self, current_time):
        self.rocket_manufacturing
        rounded_current_time = round_off_wi_exceed(current_time)
        if self.next_departure_time and round_off_wi_exceed(self.next_departure_time) == rounded_current_time:
            self.update_departure(current_time)

    
    def add_rocket_form(self, rocket_form: 'RocketForm', time: float):
        if not self.lauch_that_is_running:
            self.generate_next_departure_launchpad(time)
            rocket_form.departure_time_launchpad = self.next_departure_time
            self.lauch_that_is_running = rocket_form
        else:
            self.rocket_in_queue.append(rocket_form)
    
    def update_departure(self, time):
        self.lauch_that_is_running = None
        self.next_departure_time = None
        if self.rocket_in_queue:
            next_launch: 'RocketForm' = self.rocket_in_queue.pop(0)
            self.generate_next_departure_launchpad(time)
            next_launch.set_departure_time_launchpad(self.next_departure_time)
            self.lauch_that_is_running = next_launch


    
class RocketManufacturing:
    def __init__(self, lambda_value, closing_time):
        self.rocket_being_manufactured = None
        self.lambda_value = lambda_value
        self.closing_time = closing_time
        self.pending_rockets_to_be_manufactured = []
        self.next_arrival_time = generate_waiting_time()
        self.next_departure_time = None


    @property
    def number_of_rockets(self):
        l = len(self.pending_rockets_to_be_manufactured)
        if self.rocket_being_manufactured:
            l +=1
        return l

    def add_rocket_form(self, current_time: float):
        rocket_form  = RocketForm(current_time)
        if not self.rocket_being_manufactured:
            self.generate_next_departure(current_time)
            rocket_form.set_departure_time_manufacturing(self.next_departure_time)
            self.rocket_being_manufactured = rocket_form
            
        else:
            self.pending_rockets_to_be_manufactured.append(rocket_form)
        if current_time < self.closing_time:
            self.generate_next_arrival(current_time)
        else:
            self.next_arrival_time = None 

    def generate_next_arrival(self, current_time: float):
        self.next_arrival_time = generate_waiting_time(self.lambda_value) +  current_time
    
    def generate_next_departure(self, current_time: float):
        self.next_departure_time = generate_waiting_time(self.lambda_value) + current_time

    def update_out_of_time(self, current_time):
        rounded_current_time = round_off_wi_exceed(current_time)
        if self.next_departure_time and round_off_wi_exceed(self.next_departure_time) == rounded_current_time:
            self.update_departure(current_time)

    def update_departure(self, time):
        self.rocket_being_manufactured = None
        self.next_departure_time = None
        if self.pending_rockets_to_be_manufactured:
            rocket_form: 'RocketForm' = self.pending_rockets_to_be_manufactured.pop(0)
            self.generate_next_departure(time)
            rocket_form.departure_time_manufacturing = self.generate_next_departure
            self.rocket_being_manufactured = rocket_form