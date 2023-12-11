from intersections.intersection import Intersection

class AutoIntersection(Intersection):

    def __init__(self, id: str, center: list[float], visibility: float) -> None:
        super().__init__(id, center, visibility)