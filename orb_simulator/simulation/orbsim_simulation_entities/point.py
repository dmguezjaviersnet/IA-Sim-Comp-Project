from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
    # connected_points = []
    
    @property
    def degree(self):
        return len(self.connected_points)

    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y
    
    def __gt__(self, other: 'Point'):
        if isinstance(other, Point):
            return self.x > other.x or self.y > other.y

    def __lt__(self, other: 'Point'):
        if isinstance(other, Point):
            return self.x < other.x or self.y < other.y

    def __eq__(self, other: 'Point') -> bool:
        if isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        return False
    
    def __ne__(self, other: object) -> bool:
        if isinstance(other, Point):
            return not(other.x == self.x and other.y == self.y)
        return True
    def __hash__(self) -> int:
        return hash((self.x,self.y))
    
    def trace_line(self, other: 'Point'):
        if other not in self.connected_points:
            self.connected_points.append(other)