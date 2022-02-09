import simpy
import uuid
from orbsim_simulation_entities.elements_3d import Vector3


# Esta clase me representa un objeto de la simulacion, es la clase
# mas "abstracta" de la representacion de los objetos del environment 


class OrbsimObj:
  def __init__(self, position:Vector3, unique_id, weith:float=1, diameter:int=1,name=None):
    '''
    Este es la inicializacion de un objeto de la simulacion 

    Entrada: 
    posicion       => posicion del objetos con un vector3d 
    identificador  => un id global para saber donde esta el objeto de la
    peso           => para saber el peso del objeto de la
    diametro       => para saber la longitud de los objetos en su region mas alejada del centro 
    '''
    
    # el peso de los objetos
    self.weith: float = weith
    
    # la posicion del objeto en el espacio
    self.position: Vector3 = position

    # diametro del obejto 
    self.diameter: int = diameter

    # un nombre para el objeto 
    self.name: str = name

    # un identficador para el objeto 
    self.unique_id = unique_id

  # Este metodo dado una instancia del environmet espera un tiempo determinado 
  # y depues mueve el objeto a una posicion random  
  def move (self, env: simpy.Environment)-> None:
    self.position = Vector3.random()
    pass

  # genera un objeto random en una posicion random
  def randomObject():
    rnd = Vector3.random()
    obj_id = uuid.uuid4()
    obj = OrbsimObj(position= rnd, unique_id= obj_id)
    return obj
  
  def randomObject(max):
    rnd = Vector3.random(max)
    obj_id = uuid.uuid4()
    obj = OrbsimObj(position= rnd, unique_id= obj_id)
    return obj


  def __str__(self) -> str:
    return 'name: ' + str(self.name) + ' weith: ' + str(self.weith) + ' position: ' + str(self.position) + '  diameter: ' + str(self.diameter)
