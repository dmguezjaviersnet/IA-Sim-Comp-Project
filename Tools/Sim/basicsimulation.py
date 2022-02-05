import random 
import math
import simpy
from octree import Octree
from objects import * 
from agent import * 
from elements3d import *

NUMERO_INICIAL_OBJETOS = 10
TOTAL_COHETES = 1000
NUMERO_PLATAFORMAS = 1 
NUMERO_FABRICAS = 2
MIN_ESPERA_COHETE = 200 
MAX_ESPERA_COHETE = 300
T_LLEGADAS = 20 


def principal (env: simpy.Environment,launchpads: simpy.Store , factories : simpy.Store , objects: simpy.Store):
  for i in range (TOTAL_COHETES):
    R = random.random()
    delay = -300 * math.log(R)
    yield env.timeout(delay)
    curr_factory = random.choice(factories.items)
    curr_rocket = yield env.process(curr_factory.produceRocket(env))
    curr_launchpad = random.choice(launchpads.items)
    env.process(curr_launchpad.launchrocket(curr_rocket,objects))

# environment para correr la simulacion 
env = simpy.Environment()


# guardando en un store objetos random para tener una cantidad 
# NUMERO_INICIAL_OBJETOS en la simulacion antes de que empiece a correr
def creatingInitialObject (store: simpy.Store):
  for  item in [generateObj() for i in range (NUMERO_INICIAL_OBJETOS)]:
    store.put(item)

# guardando en un store una cantidad NUMERO_FABRICAS inicial de 
# fabricas para que puedan interactuar inicialmente con el environment 
def creatingInitialFactories (store: simpy.Store):
  for item in [factory(Vector3.random()) for i in range (NUMERO_FABRICAS)]:
    store.put(item)
  
# guardando en un store una cantidad NUMERO_PLATAFORMAS inicial de
# fabricas para que puedan interactuar inicialmente con el environmet  
def creatingInitialLaunchpad(store: simpy.Store):
  for item in [launchpad(env) for i in range(NUMERO_PLATAFORMAS)]:
    store.put(item)


def checkcollitions (objects : List[OrbsimObj]):

  WORLD_SIZE = 100

  octree = Octree(worldSize=WORLD_SIZE)

  collitionsObj = []

  #insert objetct in octree 
  for item in objects:
    position = (item.position.x,
                item.position.y,
                item.position.z)
    octree.insertNode(position, item)

  # for node in octree.iterateDepthFirst():
  #   if len(node.data) > 1 :
  #     collitionsObj += node.data

  return collitionsObj


# poner a moverse a los objetos que fueron creados inicialmente en la simulacion 
def creatingProcessToMOveObjects(env: simpy.Environment , objects: List[OrbsimObj]):
  for item in objects:
    env.process(item.move(env))


OBJECTS = simpy.Store(env)
FACTORIES = simpy.Store(env)
LAUNCHPAD = simpy.Store(env) 


creatingInitialObject(OBJECTS)
creatingInitialFactories(FACTORIES)
creatingInitialLaunchpad(LAUNCHPAD)

creatingProcessToMOveObjects(env,OBJECTS.items)

env.process(principal(env,LAUNCHPAD,FACTORIES,OBJECTS))
env.run()


# for item in OBJECTS.items:
#   print (item)

# collections = checkcollitions(OBJECTS.items)

# print('-'*10, 'Collections', '-'* 10)

# for item in collections:
#   print(item)