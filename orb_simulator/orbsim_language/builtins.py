from orbsim_language.orbsim_ast.string_node import StringNode
from orbsim_language.instance import Instance
from orbsim_language.orbsim_type import*
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

builtins_methods={
    ('String','concat'): concat,
    ('String','len'): orb_len,
    ('List', 'len'): orb_len,
    ('List', 'add'): add,
    ('List', 'remove'): remove
}

builtins_functions = {
    'randint': randint,
    'randfloat': randfloat
}