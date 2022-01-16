import random 
import math
from pkg_resources import Environment 
import simpy
from octree import Octree
from objects import * 
import uuid 
from agent import * 
from elements3d import * 

NUMERO_INICIAL_OBJETOS = 1
TOTAL_COHETES = 1000
NUMERO_PLATAFORMAS = 1 
NUMERO_FABRICAS = 2
MIN_ESPERA_COHETE = 200 
MAX_ESPERA_COHETE = 300
T_LLEGADAS = 200


def lanzar(cohete):
  R = random.random()
  tiempo = MAX_ESPERA_COHETE - MIN_ESPERA_COHETE
  tiempo_lanzamiento  = MIN_ESPERA_COHETE + (tiempo * R)
  yield env.timeout(tiempo_lanzamiento)
  print("\o/  %s lanzado con exito en %.2f minutos" %(cohete,tiempo_lanzamiento)) 

def launch_rocket(env,name,plataformas):
  llega = env.now
  print('---> %s llego a plataforma en minuto %.2f' %(name,llega))
  with plataformas.request() as request:
    yield request 
    pasa = env.now
    espera = pasa - llega
    print('*** %s pasa a la plataforma de lanzamiento en el minuto %.2f habiendo esperado %.2f minutos ' %(name,llega,espera))
    yield env.process(lanzar(name))

def principal (env: simpy.Environment,launchpads: simpy.Store , factories : simpy.Store , objects: simpy.Store):
  # llegada = 0
  # for i in range(TOTAL_COHETES):
  #   R = random.random()
  #   llegada = -T_LLEGADAS * math.log(R)
  #   yield env.timeout(llegada)
  #   env.process(launch_rocket(env,'Cohete %d' % (i+1), plataformas))
  for i in range (TOTAL_COHETES):
    R = random.random()
    delay = -300 * math.log(R)
    yield env.timeout(delay)
    curr_factory = random.choice(factories.items)
    curr_rocket = yield env.process(curr_factory.produceRocket(env))
    curr_launchpad = random.choice(launchpads.items)
    env.process(curr_launchpad.launchrocket(curr_rocket,objects))


env = simpy.Environment()
# plataformas = simpy.Resource(env,NUMERO_PLATAFORMAS)
 

# env.process(principal(env,LAUNCHPAD))
# env.run()

def creatingInitialObject (store: simpy.Store):
  for  item in [generateObj() for i in range (NUMERO_INICIAL_OBJETOS)]:
    store.put(item)

def creatingInitialFactories (store: simpy.Store):
  for item in [factory(Vector3.random()) for i in range (NUMERO_FABRICAS)]:
    store.put(item)
  
def creatingInitialLaunchpad(store: simpy.Store):
  for item in [launchpad(env) for i in range(NUMERO_PLATAFORMAS)]:
    store.put(item)


def creatingProcessToMOveObjects(env: simpy.Environment , objects: List[obj]):
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