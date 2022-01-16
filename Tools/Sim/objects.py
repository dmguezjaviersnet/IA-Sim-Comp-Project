from typing import *
from elements3d import Vector3
import uuid
import simpy


# Esta clase me representa un objeto de la simulacion, es la clase
# mas "abstracta" de la representacion de los objetos del environment 
class obj:
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
    while True:
      yield env.timeout(200)
      self.position = Vector3.random()
      print ('El objeto %s se ha movido a la posicion %s' %(str(self.unique_id), str(self.position)))


  def __str__(self) -> str:
    return 'name: ' + str(self.name) + ' weith: ' + str(self.weith) + ' position: ' + str(self.position) + '  diameter: ' + str(self.radius)

# Esta clase me repesenta un Cohete en la simulacion , un cohete puede
# contener una lista de satelite 
class Rocket(obj):
  def __init__(self, position: Vector3, unique_id, weith: float = 1, diameter: int = 1, name=None, fuel:float= 100 , satellites: List['Satellite']=[]):
    super().__init__(position, unique_id, weith=weith, diameter=diameter, name=name)

    # este es el combustible del cohete 
    self.fuel: float = fuel

    # esta es la lista de satelites que contiene el cohete 
    self.satellites: Satellite = satellites

    # esta es la vida del cohete 
    self.life = 100

# Esta clase me representa un satelite en la simulacion 
class Satellite(obj):
  def __init__(self, position: Vector3, unique_id, weith: float = 1, diameter: int = 1, name=None):
    super().__init__(position, unique_id, weith=weith, diameter=diameter, name=name)
    '''
    inicializacion de los satelites , se llama a la clase padre 
    para inicializar los valores que se pasan en los parametros 
    '''

# esto es para generar objetos aleatorios de la simulacion 
def generateObj ():
  unique_id = uuid.uuid4()
  position = Vector3.random()
  new_obj = obj(position=position,unique_id= unique_id)
  return new_obj