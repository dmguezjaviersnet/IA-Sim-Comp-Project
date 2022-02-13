from simulation.orbsim_simulation_entities.agent import Agent
from simulation.orbsim_simulation_entities.elements_3d import Vector3
from enum import Enum

class STATUSCOLLECTOR(Enum):
  FULL = 0 
  EXHAUSTED = 1
  HALFFULL =2 


class Collectors(Agent):
  def __init__(self, loc: Vector3, unique_id, params) -> None:
    super().__init__(loc, unique_id, params)
    self.status = STATUSCOLLECTOR.HALFFULL
  

  def _getdetermination():
    det = [(STATUSCOLLECTOR.FULL , 'empty'),
          (STATUSCOLLECTOR.EXHAUSTED, 'descend'),
          (STATUSCOLLECTOR.HALFFULL,'collect')]
    return det

  def _rejuvenate(self):
    pass

  def _emptyCollector():
    pass

  def _collect(self):
    pass

  def collectgarbage(self):
    determ = self._getdetermination()
    for status in determ:
      if status[0] == STATUSCOLLECTOR.FULL:
        self._emptyCollector()
      elif status[0] == STATUSCOLLECTOR.EXHAUSTED:
        self._rejuvenate()
      elif status[0] == STATUSCOLLECTOR.HALFFULL:
        self._collect()