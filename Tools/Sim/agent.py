from logging import root
import random
from typing import *
import math
from enum import Enum
from objects import *
import numpy as np 
import uuid
import simpy
from elements3d import * 

T_BUILD_ROCKET = 200
T_BUILD_SATELLITE = 100
T_WAITING_TO_INTERACT = 100

class Agent: 
  def __init__(self, loc:Vector3 , unique_id,params) -> None:
    """Create a new agent in the given location.
    
    loc: tuple coordenates 
    params: dictionary of parameters
    """
    self.loc: Vector3 = loc
    self.age:int  = 0 
    self.unique_id : uuid.UUID = unique_id

    # extract the parameter 
    min_lifespan: int = params.get('min_lifespan', 100000)
    max_lifespan: int = params.get('max_lifespan', 100000)

    self.lifespan = np.random.uniform(min_lifespan,max_lifespan)


class RocketQuality(Enum):
  VERYGOOD = 0 
  GOOD = 1
  REGULAR = 2
  BAD = 3
  VERYBAD = 4


# clase que representa una fabrica, que produce satelites y cohetes  
class factory():
  def __init__(self, loc:Vector3 ) -> None:
    self.age: int  = 0 
    
    # localizacion de la fabrica
    self.loc: int = loc
    # ranking de la fabrica 
    self.ranking : int = 0 

  # esta metodo crea nuevos satelites para ser enviados a la orbita 
  def produceSatellite(self, env : simpy.Environment, quiality : int = None) -> Satellite:
    # tiempo en que se comenzo a producir los cohetes 
    start_pro = env.now
    R = random.random()
    
    #tiempo que va a durar en construirse el cohete  
    t_const = -T_BUILD_SATELLITE * math.log(R)
    yield env.timeout(t_const)

    # creandole una nueva posicion al satelite 
    pos_satellite = Vector3.Zero()
    
    # generar un id para el nuevo satelite 
    id_satellite = uuid.uuid4()

    # darle un peso a el nuevo satelite 
    weith_satellite = random.random() * 100
    
    # se crea el nuevo satelite 
    new_satellite = Satellite(pos_satellite,
                              id_satellite,
                              weith_satellite)
    end_pro = env.now

    #aumenting ranking of Factory    
    self.ranking = self.ranking + 1 
    print("+++ Producido con exito el satelite con id (%s) en %.2f minutos" %(str(new_satellite.unique_id),end_pro - start_pro)) 
    
    # se retorna en el proceso el nuevo satelite 
    return new_satellite

  # metodo para producir un nuevo cohete, ese cohete  tiene que tener una lista de 
  # satelites que van as ser lanzados al espacio 
  def produceRocket(self,env : simpy.Environment,quality: int = None) -> Rocket:
    
    # tiempo en el que empezo a producice el cohete 
    start_pro = env.now
    R = random.random()
    t_const = -T_BUILD_ROCKET * math.log(R)
    yield env.timeout(t_const)

    # crea un nuevo proceso y espera por este para  construir un nuevo satelite  
    new_satellite = yield env.process(self.produceSatellite(env))

    # generar un nuevo id para el nuevo cohete creado 
    rocket_id = uuid.uuid4()
    rocket = Rocket(self.loc,rocket_id,satellites=[new_satellite])
    
    #aumenting  ranking of Factory 
    self.ranking = self.ranking + 1 
    end_pro = env.now 
    print("+++ Producido con exito el cohete con id: (%s) en: %.2f minutos" %(str(rocket.unique_id),end_pro - start_pro)) 
    return rocket


# Esta es una clase para representar las plataformas de lanzamiento
class launchpad:
  def __init__(self,env: simpy.Environment, quality: int = 10, amount_plataforms: int= 1) -> None:
    
    # inicializando la edad de la plataforma 
    self.age: int = 0   
    
    # guardando uan instancia de un Environment
    self.env: simpy.Environment = env
    
    # Poniendo una clasificacion para la estacion de lanzamiento 
    self.quality : int = quality

    # cantidad de plataformas de lanzamiento del la base de lanzamiento  
    self.amount_plataforms : int  = amount_plataforms

    # recuros de simpy que te representa las plataformas de lanzamiento que hay 
    # en la base , estas platafomas son 1 o mas en dependencia de la cantiad que se decida
    self.plataforms : simpy.Resource = simpy.Resource(env,amount_plataforms)

    # poniendole un identificador para representar la plataforma entre 
    # los objetos globales de la simulacion 
    self.unique_id : uuid.UUID = uuid.uuid4()

  # este proceso se llama para simular el lanzamiento de un cohete a la orbita 
  def launchrocket (self,rocket: Rocket ,storeobjects : simpy.Store):
    
    # tiempo de arrivo del cohete a la plataforma 
    arrive = self.env.now 
    print('---> el cohete %s llego a plataforma [%s] en el minuto %.2f' %(str(rocket.unique_id),str(self.unique_id),arrive))
    
    # se hace un request para pedir un recurso que sea una de las plataformas 
    # para lanzar el cohete 
    with self.plataforms.request() as request:
      yield request

      # el tiempo e el que va a ser lanzada la plataforma 
      go_launch = self.env.now
      # el tiempo que estuvo esperando para ser lanzado a la orbita 
      delay = go_launch - arrive 
      print('*** %s pasa a la plataforma de lanzamiento [%s] en el minuto %.2f habiendo esperado %.2f minutos ' %(str(rocket.unique_id),str(self.unique_id),arrive,delay))
      yield self.env.process(self.trakingflight(rocket,storeobjects))

  # Este metodo es para simular el tiempo que el cohete se demora
  # en llegar a la atmosfera, todo esto ocurre en un intervalo de tiempo random 
  def trakingflight (self, rocket: Rocket, storeobjects: simpy.Store):
    
    # tiempo en que despega el cohete 
    takeoff_time = self.env.now
    R = random.random()

    # tiempo de vuelo del cohete (este es el tiempo desde que despega 
    # hasta que llega a la orbita baja )
    rise_time = -400 * math.log(R)
    yield  self.env.timeout(rise_time)

    # hacer un recorrido por todos los satelites y enviarlos al
    # al espacio para hacer que todos los satelites que trae el
    # cohete entre en sus orbitas correspondientes
    for curr_satellite in rocket.satellites:
      storeobjects.put(curr_satellite)
      print('+++ %s lanzado con exito a la orbita en el minuto %.2f' % (str(curr_satellite.unique_id),self.env.now))
      self.env.process(curr_satellite.move(self.env))


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