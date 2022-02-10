from dataclasses import dataclass
from typing import Any, Dict

from telegram import Dice
from orbsim_language.orbsim_type import OrbsimType


class Instance:
    
    def __init__(self, orbsim_type: OrbsimType, value = None):
        self.orbsim_type =  orbsim_type
        self.value = value if value != None else id(self)
        self.attributes_vals: Dict[str, 'Instance']  = {}


    def set_attr_instance(self, attr_name: str, value: 'Instance'):
        self.attributes_vals[attr_name] =  value
    
    def get_attr_instance(self, attr_name: str):
        return self.attributes_vals[attr_name]
    
    



    
    


