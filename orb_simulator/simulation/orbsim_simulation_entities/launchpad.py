import simpy 
import uuid
import random 
import math
from orbsim_simulation_entities.rocket import Rocket

class Launchpad:
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