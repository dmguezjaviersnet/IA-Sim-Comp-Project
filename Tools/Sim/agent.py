from typing import *
from Vector3 import * 
import numpy as np 

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

