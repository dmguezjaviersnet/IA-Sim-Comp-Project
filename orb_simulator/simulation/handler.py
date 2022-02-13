import simpy
import random 
import numpy as np
from typing import List
from simulation.orbsim_simulation_structs.octree import Octree
from simulation.orbsim_simulation_entities import OrbsimObj , Factory , Vector3 , Launchpad , Junk
from colorama import Back, Fore, init


class Handler:
  def __init__(self,world_size = 1024,
                    world_depth = 10,
                    amount_initial_obj= 100,
                    amount_rockets = 10,
                    amount_launchpads = 2,
                    amount_factories = 4, 
                    delay_move_object= 1000):
    self._env = simpy.Environment()
    self._world_size = world_size
    self._world_depth = world_depth
    self._delay_move_object = delay_move_object
    self._amount_initial_obj = amount_initial_obj
    self._amount_rockets = amount_rockets
    self._amount_launchpads =amount_launchpads
    self._amount_factories = amount_factories 
    self._objects = self._generate_objects() 
    self._factories = self._generate_factories()
    self._launchpads = self._generate_launchpads()
    self._end_simulation = self._env.event()


  def main (self):
    for i in range (self._amount_rockets):

      # creando un timepo para el lanzamiento entre un cohete y otro 
      R = random.random()
      delay = -300 * np.log(R)
      yield self._env.timeout(delay)


      curr_factory = random.choice(self._factories)
      curr_rocket = yield self._env.process(curr_factory.produceRocket(self._env))
      curr_launchpad = random.choice(self._launchpads)
      self._env.process(curr_launchpad.launchrocket(curr_rocket,self._objects))

  def check_collitions(self):

    octree = Octree(world_size= self._world_size,
                    origin= Vector3.Zero(),
                    max_type= None,
                    max_value= 6)
    
    for item in self._objects:
      octree.insertNode(item.position, item)

    collitions_obj = []
    for node in octree.iterateDepthFirst():
      if node.isLeafNode and (len(node.data)> 1):
        collitions_obj += [node.data]

    return collitions_obj

  def generate_garbage_from_a_collition (self, collition_objects: List[OrbsimObj]):
    
    total_weith = 0

    for obj in collition_objects:
      total_weith += obj.weith
    
    # ver despues la cantidad de objetos en que se puede dividir
    # todos los objetos a partir de los objeto que colisionaron
    
    r = random.random()
    a = - len(collition_objects) * np.log(r)
    b = - len(collition_objects) * np.log(a)

    new_junk = [] 

    ## arreglar esto despues
    for i in range(int(b)):
      ## arreglar el random despues
      new_junk.append(Junk.random(100))
    
    return new_junk
 

  def move_and_check_collitions(self):
    while True:
      yield self._env.timeout(self._delay_move_object)

      ## moviendo todos los objetos a la proxima posicion 

      for obj in self._objects:
        obj.move(self._env)
      
      collitions = self.check_collitions()

      if collitions: 

        # print (Fore.RED, '-'*10, 'Hubo una colision entre los objetos','-'*10)
        # for item in collitions:
        #   print ('[', [str(i) for i in item] ,']')
        # print('-' * 55 , Fore.RESET)

        count_junk = 0 
        for item in collitions:
          new_junk = self.generate_garbage_from_a_collition(item)
          count_junk += len(new_junk) 
          self._objects  = self._objects + new_junk
        
        # print ('se generaron' , count_junk, 'objetos que son basura')


  def _addProcess(self):
    self._env.process(self.move_and_check_collitions())
    self._env.process(self.main())

  def _generate_objects(self):
    return [OrbsimObj.random(self._world_size) for i in range (self._world_size)]
  
  def _generate_factories(self):
    return [Factory(Vector3.random(self._world_size)) for i in range(self._amount_factories)]

  def _generate_launchpads(self):
    return [Launchpad(self._env) for i in range(self._amount_launchpads)]

  def start(self):
    self._addProcess()
    self._env.run(until= self._end_simulation)
  
  def stop (self):
    self._end_simulation.succeed()

  # puede ser usado para annadir un nuevo lugar de lanzamiento
  def add_lauchpad(self):
    new_launchpad = Launchpad(self._env)
    self._lauchpad.append(new_launchpad)
    self._amount_launchpads += 1

  # esto puede ser usado para annadir un nuevo objeto a la simulacion 
  def add_objetc(self):
    new_object = OrbsimObj.random(self._world_size)
    self.objects.append(new_object)

  # esto puede ser llamado para annadir una nueva fabrica
  def add_factory(self):
    new_factory = Factory(Vector3.random(self._world_size))
    self._factories.append(new_factory)
    self._amount_factories+=1



if __name__ == '__main__':

  handler = Handler()

  while True:
    cmd = input('give me command: ')

    if cmd == 'start':
      handler.start()
    if cmd == 'stop':
      handler.stop()
    if cmd == 'exit':
      break
  
  print ('end simulation')