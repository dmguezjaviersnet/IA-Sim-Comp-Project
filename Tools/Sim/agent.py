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

class Agent: 
  def __init__(self, loc:Vector3 , unique_id,params) -> None:
    """Create a new agent in the given location.
    
    loc: tuple coordenates 
    params: dictionary of parameters
    """
    self.loc = loc
    self.age = 0 
    self.unique_id = unique_id

    # extract the parameter 
    min_lifespan = params.get('min_lifespan', 100000)
    max_lifespan = params.get('max_lifespan', 100000)

    self.lifespan = np.random.uniform(min_lifespan,max_lifespan)

class RocketQuality(Enum):
  VERYGOOD = 0 
  GOOD = 1
  REGULAR = 2
  BAD = 3
  VERYBAD = 4


class factory():
  def __init__(self, loc:Vector3 ) -> None:
    self.age = 0 
    self.loc = loc
    self.ranking = 0 

  def produceSatellite(self, env, quiality = None):
    start_pro = env.now
    R = random.random()
    t_const = -T_BUILD_SATELLITE * math.log(R)
    yield env.timeout(t_const)
    pos_satellite = Vector3.Zero()
    id_satellite = uuid.uuid4()
    weith_satellite = random.random() * 100
    new_satellite = Satellite(pos_satellite,
                              id_satellite,
                              weith_satellite)
    end_pro = env.now
    #aumenting ranking of Factory
    self.ranking = self.ranking + 1 
    print("+++ Producido con exito el satelite con id (%s) en %.2f minutos" %(str(new_satellite.unique_id),end_pro - start_pro)) 
    return new_satellite

  def produceRocket(self,env,quality = None):
    start_pro = env.now
    R = random.random()
    t_const = -T_BUILD_ROCKET * math.log(R)
    yield env.timeout(t_const)
    # building a new satellite 
    new_satellite = yield env.process(self.produceSatellite(env))
    # building a new satellite 

    rocket_id = uuid.uuid4()
    rocket = Rocket(self.loc,rocket_id,satellites=[new_satellite])
    #aumenting  ranking of Factory 
    self.ranking = self.ranking + 1 
    end_pro = env.now 
    print("+++ Producido con exito el cohete con id: (%s) en: %.2f minutos" %(str(rocket.unique_id),end_pro - start_pro)) 
    return rocket

class launchpad:
  def __init__(self,env , quality = 10, amount_plataforms= 1) -> None:
    self.age = 0 
    self.quality = quality
    self.amount_plataforms = amount_plataforms
    self.plataforms = simpy.Resource(env,amount_plataforms)
    self.unique_id = uuid.uuid4()

  def launchrocket (self, env, rocket: Rocket):
    arrive = env.now 
    print('---> %s llego a plataforma [%s] el cohete en el minuto %.2f' %(str(rocket.unique_id),str(self.unique_id),arrive))
    with self.plataforms.request() as request:
      yield request
      go_launch = env.now
      delay = go_launch - arrive 
      print('*** %s pasa a la plataforma de lanzamiento [%s] en el minuto %.2f habiendo esperado %.2f minutos ' %(str(rocket.unique_id),str(self.unique_id),arrive,delay))
      

