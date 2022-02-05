import random 
import simpy
import uuid
import math
from orbsim_simulation_entities.satellite import Satellite
from orbsim_simulation_entities.elements_3d import Vector3
from orbsim_simulation_entities.conf_variables import T_BUILD_SATELLITE


class Factory():
  def __init__(self, loc: Vector3 ) -> None:
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