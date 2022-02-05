import uuid
import random 
import math
import simpy
from typing import List
from orbsim_simulation_entities.elements_3d import Vector3


# Esta clase representa a una persona que es un agente
# que va a interactuar con los demas agentes de la simulacion 
class Person(Agent):
  def __init__ (self, loc: Vector3 , unique_id: uuid.UUID):
    super().__init__(loc, unique_id)

  # Para interactuar con las demas agentes y generar nuevos objetos simulacion
  # digamos satelites para poder annadir mas elementos a la simulacion 
  def toInteract (self, env: simpy.Environment, factories: List[factory], launchpads : List[launchpad],objects = simpy.Store):
    while True:
      R = random.random()
      delay = - T_WAITING_TO_INTERACT * math.log(R)
      # esperando un tiempo a que el satelite salga y llegue a la orbita
      yield env.timeout(delay)

      # decide to create a Rocket
      curr_fact = random.choice(factories)

      # contriur un nuevo cohete
      curr_rocket = yield env.process(curr_fact.produceRocket(env,quality=5))

      # escoger un nuevo cohete 
      curr_launch = random.choice(launchpads)

      # crear un nuevo proceso para llamar a lanzar el cohete 
      yield env.process(curr_launch.launchrocket(curr_rocket,objects))
      print('+++ ^^^ La persona %s mando a lanzar el cohete %s en el minuto %.2f' % (str(self.unique_id),str(curr_rocket), env.now))