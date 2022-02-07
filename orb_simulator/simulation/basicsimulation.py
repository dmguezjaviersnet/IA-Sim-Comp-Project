import random 
import math
from typing import List
import simpy
from sympy import O
from orbsim_simulation_structs import Octree
from orbsim_simulation_entities import Agent , OrbsimObj, Factory , Vector3 , Launchpad
import uuid
from colorama import Back, Fore, init

#init colorama
init()


NUMERO_INICIAL_OBJETOS = 10
TOTAL_COHETES = 10
NUMERO_PLATAFORMAS = 1 
NUMERO_FABRICAS = 2
MIN_ESPERA_COHETE = 200 
MAX_ESPERA_COHETE = 300
T_LLEGADAS = 20 

def generateObj():
  rnd = Vector3.random()
  obj_id = uuid.uuid4()
  obj = OrbsimObj(position=rnd,unique_id= obj_id)
  return obj



def principal (env: simpy.Environment,launchpads: simpy.Store , factories : simpy.Store , objects: simpy.Store):
  for i in range (TOTAL_COHETES):
    R = random.random()
    delay = -300 * math.log(R)
    yield env.timeout(delay)
    curr_factory = random.choice(factories)
    curr_rocket = yield env.process(curr_factory.produceRocket(env))
    curr_launchpad = random.choice(launchpads)
    env.process(curr_launchpad.launchrocket(curr_rocket,objects))

# environment para correr la simulacion 
env = simpy.Environment()


# guardando en un store objetos random para tener una cantidad 
# NUMERO_INICIAL_OBJETOS en la simulacion antes de que empiece a correr
def creatingInitialObject (store: simpy.Store):
  # for  item in [generateObj() for i in range (NUMERO_INICIAL_OBJETOS)]:
  #   store.put(item)
  return [generateObj() for i in range (NUMERO_INICIAL_OBJETOS)]

# guardando en un store una cantidad NUMERO_FABRICAS inicial de 
# fabricas para que puedan interactuar inicialmente con el environment 
def creatingInitialFactories (store: simpy.Store):
  for item in [Factory(Vector3.random()) for i in range (NUMERO_FABRICAS)]:
    store.put(item)
  
# guardando en un store una cantidad NUMERO_PLATAFORMAS inicial de
# fabricas para que puedan interactuar inicialmente con el environmet  
def creatingInitialLaunchpad(store: simpy.Store):
  for item in [Launchpad(env) for i in range(NUMERO_PLATAFORMAS)]:
    store.put(item)


def difference_objects(objects : List[OrbsimObj], collisions_obj : List[OrbsimObj]):
  set_objects = set (objects)
  set_collitions = set([item for item1 in collisions_obj for item in item1])  

  differences = set_objects.difference(set_collitions)

  return list(differences)

def check_collitions (objects : List[OrbsimObj]):

  WORLD_SIZE = 1024

  origin = Vector3.Zero()

  octree = Octree(worldSize=WORLD_SIZE,origin=origin , max_type= None, max_value=6)

  collitionsObj = []

  #insert object in octree 
  for item in objects:
    octree.insertNode(item.position, item)

  for node in octree.iterateDepthFirst():
    if node.isLeafNode and  (len(node.data) > 1 ):
      collitionsObj += [node.data]

  return collitionsObj


def moveAndCheckCollitions(env: simpy.Environment, objects : List[OrbsimObj]):
  while True:
    yield env.timeout(100)
    for item in objects:
      item.move(env)
    
    collitions = check_collitions(objects)
    if collitions:

      print (Fore.RED, '-'*10, 'hubo una colision entre los objetos','-'*10)
      for item in collitions:
        print ('[', [str(i) for i in item], ']')
      print ('-'*50)
      print(Fore.RESET)

      objects = difference_objects(objects, collitions)

      print ('se elimino al objeto '  , collitions)

# poner a moverse a los objetos que fueron creados inicialmente en la simulacion 
def creatingProcessToMOveObjects(env: simpy.Environment , objects: List[OrbsimObj]):
  for item in objects:
    env.process(item.move(env))
 


OBJECTS = [generateObj() for i in range (NUMERO_INICIAL_OBJETOS)]
FACTORIES = [Factory(Vector3.random()) for i in range (NUMERO_FABRICAS)]
LAUNCHPAD = [Launchpad(env) for i in range(NUMERO_PLATAFORMAS)]

env.process(moveAndCheckCollitions(env,OBJECTS))

env.process(principal(env,LAUNCHPAD,FACTORIES,OBJECTS))
env.run()

