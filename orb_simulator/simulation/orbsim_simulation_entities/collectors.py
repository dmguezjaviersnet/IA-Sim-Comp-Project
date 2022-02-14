from orbsim_simulation_entities.agent import Agent
from orbsim_simulation_entities.elements_3d import Vector3, Vector2
from enum import Enum

class STATUSCOLLECTOR(Enum):
  FULL = 0 
  EXHAUSTED = 1
  HALFFULL =2 


class Collectors(Agent):
  def __init__(self, position: Vector3, unique_id, params) -> None:
    super().__init__(position, unique_id, params)
    self.status = STATUSCOLLECTOR.HALFFULL
    self._way_to_go = []
  

  def _get_determination():
    det = [(STATUSCOLLECTOR.FULL , 'empty'),
          (STATUSCOLLECTOR.EXHAUSTED, 'descend'),
          (STATUSCOLLECTOR.HALFFULL,'collect')]
    return det

  def _rejuvenate(self, env):
    pass 


  def move (self):
    if len(self._way_to_go) > 0 :      
      next_move = self._way_to_go.pop(0)
      self.position = Vector3(next_move.x, next_move.y)
    else: 
      self.position = Vector3.random(100)


  def _emptyCollector(self, env):
    position2d = Vector2(self.position.x, self.position.y)
    launcpad_more_close = env.get_the_most_close_launcpad(position2d)
    walk = env.get_the_best_way (position2d, Vector2(launcpad_more_close.position.x, launcpad_more_close.position.y))
    self._way_to_go = walk


  def _collect(self):
    pass

  def collectgarbage(self):
    determ = self._get_determination()
    for status in determ:
      if status[0] == STATUSCOLLECTOR.FULL:
        self._emptyCollector()
      elif status[0] == STATUSCOLLECTOR.EXHAUSTED:
        self._rejuvenate()
      elif status[0] == STATUSCOLLECTOR.HALFFULL:
        self._collect()