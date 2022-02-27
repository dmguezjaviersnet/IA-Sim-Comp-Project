from orbsim_language.orbsim_ast.string_node import StringNode
from orbsim_language.instance import Instance
from orbsim_language.orbsim_type import*
from orbsim_pygame import PygameHandler
import random
import copy


def concat(s1: 'Instance', s2: 'Instance'):
    return Instance(StringType(), s1.value + s2.value)

def orb_len(s1: 'Instance'):
    return Instance(IntType(), len(s1.value))

def add(list: 'Instance', new_val: 'Instance'):
    new_list = copy.deepcopy(list.value)
    new_list.append(new_val.value)
    return Instance(ListType(), new_list)

def remove(list: 'Instance', val_remove: 'Instance'):
    new_list = copy.deepcopy(list.value)
    new_list.remove(val_remove.value)
    return Instance(ListType(), new_list)

def randint(inf: 'Instance', sup: 'Instance'):
    randvalue =  random.randint(inf.value, sup.value)
    return Instance(IntType(), randvalue)

def randfloat(inf: 'Instance', sup: 'Instance'):
    randvalue =  random.randrange(inf.value, sup.value)
    randvalue = random.random() + randvalue
    return Instance(IntType(), randvalue)

def orbit_add_to_simulation(o1: 'Instance', handler: 'PygameHandler'):
    handler.add_new_orbit(o1.value)

def satellite_add_to_simulation(o1: 'Instance', handler: 'PygameHandler'):
    handler.add_new_satellite(o1.value)

def space_debris_add_to_simulation(o1: 'Instance', handler: 'PygameHandler'):
    handler.add_new_space_debris(o1.value)

def for_simulation(method_name: str):
    return method_name == 'add_to_simulation'

builtins_methods={
    ('String','concat'): concat,
    ('String','len'): orb_len,
    ('List', 'len'): orb_len,
    ('List', 'add'): add,
    ('List', 'remove'): remove,
    ('Orbit', 'add_to_simulation'): orbit_add_to_simulation,
    ('Satellite', 'add_to_simulation'): satellite_add_to_simulation,
    ('SpaceDebris', 'add_to_simulation'): space_debris_add_to_simulation,
    
    

}

builtins_functions = {
    'randint': randint,
    'randfloat': randfloat
}