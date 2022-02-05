from elements_3d import Vector3

class Region:
  def __init__(self, center: Vector3 , radio : int) -> None:
    self.center = center
    self.radio = radio
  
  def __str__(self) -> str:
    return 'center :' + str(self.center)  + '  radio: ' + str(self.radio)