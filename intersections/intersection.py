from shapely import Polygon, Point

class Intersection():

    def __init__(self, id : str, center : list[float], visibility : float ) -> None:
        self.id = id
        self.center = Point(center[0], center[1])

        visibility = abs(visibility)
        a = (center[0]-visibility, center[1]-visibility)
        b = (center[0]+visibility, center[1]-visibility)
        c = (center[0]+visibility, center[1]+visibility)
        d = (center[0]-visibility, center[1]+visibility)
        self.area = Polygon((a, b, c, d))


    def contains(self, position : tuple):
        point = Point(position[0], position[1])
        return self.area.contains(point)
    
    def mutation(self, chromosom : list[float], proba : float) -> list[float]:
        return chromosom
    
    def sanitize_chromosom(self, chromosom : list[float]) -> list[float]:
        return chromosom
    
    def get_initial_chromosoms(self, n : int) -> list[list[float]]:
        return []
    
    def get_default_chromosom(self) -> list[float]:
        pass

    def apply_chromosom(self, chromosom : list[float]):
        pass

    def step_callback(*args):
        pass