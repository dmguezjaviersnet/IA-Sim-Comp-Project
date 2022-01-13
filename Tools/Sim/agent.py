from logging import root
import random
from typing import *
import math
from enum import Enum
from scipy import rand
from objects import *
from Vector3 import * 
import numpy as np 
import uuid
import simpy

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


class Factory():
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
    print("+++ Producido con exito el satelite en %.2f minutos" %(end_pro - start_pro)) 
    return new_satellite

  def produceRocket(self,env,quality = None):
    start_pro = env.now
    R = random.random()
    t_const = -T_BUILD_ROCKET * math.log(R)
    yield env.timeout(t_const)
    # building a new satellite 
    new_satellite = self.produceSatellite(env)
    # building a new satellite 
    rocket = Rocket(fuel=100, satellites= [new_satellite])
    #aumenting  ranking of Factory 
    self.ranking = self.ranking + 1 
    end_pro = env.now 
    print("+++ Producido con exito %.2f minutos" %(end_pro - start_pro)) 
    return rocket

class launchpad:
  def __init__(self, quality = 10) -> None:
    self.age = 0 
    self.quality = quality


