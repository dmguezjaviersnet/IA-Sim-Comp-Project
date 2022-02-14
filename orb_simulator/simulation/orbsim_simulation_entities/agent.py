from validators import uuid


from uuid import UUID
from orbsim_simulation_entities.elements_3d import Vector3
import numpy as np

class Agent: 
  def __init__(self, position:Vector3 , unique_id,params) -> None:
    """Create a new agent in the given location.
    
    position: tuple coordenates 
    params: dictionary of parameters
    """
    self.position: Vector3 = position
    self.age:int  = 0 
    self.unique_id : UUID = unique_id

    # extract the parameter 
    min_lifespan: int = params.get('min_lifespan', 100000)
    max_lifespan: int = params.get('max_lifespan', 100000)

    self.lifespan = np.random.uniform(min_lifespan,max_lifespan)