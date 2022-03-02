from cgitb import handler
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

def create_custom_space_debris(size: 'Instance', color: 'Instance', handler:'PygameHandler'):
    return Instance(SpaceDebrisType(), handler.create_custom_space_debris(size.value, color.value))

def number_of_satellites(handler: 'PygameHandler'):
    return Instance(IntType(), handler.number_of_satellites)

def number_of_space_debris(handler: 'PygameHandler'):
    return Instance(IntType(), handler.number_of_space_debris)

def number_of_objects(handler: 'PygameHandler'):
    return Instance(IntType(), handler.number_of_objects)

def number_of_orbits(handler: 'PygameHandler'):
    return Instance(IntType(), handler.number_of_orbits)

def build_tuple(values:List['Instance']):
    values = ()
    for i in values:
        values += (i.value,)
    return Instance(TupleType(), values)

def orbit_add_to_simulation(o1: 'Instance', handler: 'PygameHandler'):
    handler.add_new_orbit(o1.value)

def satellite_add_to_simulation(o1: 'Instance', handler: 'PygameHandler'):
    handler.add_new_satellite(o1.value)

def space_debris_add_to_simulation(o1: 'Instance', handler: 'PygameHandler'):
    handler.add_new_space_debris(o1.value)

def space_debris_move_to_orbit(sp: 'Instance', orbit: 'Instance', handler: 'PygameHandler'):
    handler.move_space_debris_to_orbit(orbit.value, sp.value)

def custom_launchpad(t:'Instance', lambda_val: 'Instance', handler: 'PygameHandler'):
    handler.launchpad_factory_closing_time = t.value
    handler.launchpad_factory_lambda = lambda_val.value

def custom_sp_poisson(t:'Instance', lambda_val: 'Instance', handler: 'PygameHandler'):
    handler.poisson_space_creation_closing_time = t.value
    handler.poisson_space_creation_lambda = lambda_val.value

simulation_names = ['add_to_simulation', 'number_objects', 'number_orbits', 
'number_space_debris', 'number_satellites', 'custom_space_debris', 'move_to_orbit', 
'custom_launchpad', 'custom_create_space_debris_event']

def for_simulation(method_name: str):
    return method_name in simulation_names

builtins_methods={
    ('String','concat'): concat,
    ('String','len'): orb_len,
    ('List', 'len'): orb_len,
    ('List', 'add'): add,
    ('List', 'remove'): remove,
    ('Orbit', 'add_to_simulation'): orbit_add_to_simulation,
    ('Satellite', 'add_to_simulation'): satellite_add_to_simulation,
    ('SpaceDebris', 'add_to_simulation'): space_debris_add_to_simulation,
    ('SpaceDebris', 'move_to_orbit'): space_debris_move_to_orbit,
    
    
    

}

builtins_functions = {
    'randint': randint,
    'randfloat': randfloat,
    'number_objects': number_of_objects,
    'number_orbits': number_of_orbits,
    'number_space_debris': number_of_space_debris,
    'number_satellites': number_of_satellites,
    'custom_space_debris': create_custom_space_debris,
    'custom_launchpad' : custom_launchpad,
    'custom_create_space_debris_event':  custom_sp_poisson
}