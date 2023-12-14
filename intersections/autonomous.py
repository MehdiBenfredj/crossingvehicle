from intersections.intersection import Intersection
import random
import sumolib

class AutoIntersection(Intersection):

    def __init__(self, id: str, center: list[float], visibility: float, max_vehicles : int) -> None:
        super().__init__(id, center, visibility)

        self.edges = self._get_edges
        self.crossing = False
        self.chromosom = []
        self.priorities = []
        self.max_vehicles = max_vehicles

    
    def _get_edges(self) -> list[str]:
        pass


    def _calc_priority(self, edge_id):
        pass
    

    def mutation(self, chromosom : list[float], proba : float) -> list[float]:

        rand_number = random.random()
        if rand_number > proba:
            return chromosom
        
        rand_index = random.randint(0, len(chromosom)-1)
        rand_number = random.random()
        if rand_number >= 0.5:
            if chromosom[rand_index] - 1 >= 1:
                chromosom[rand_index] -= 1
        else:
            chromosom[rand_index] += 1
            
        return self.sanitize_chromosom(chromosom)
    

    def sanitize_chromosom(self, chromosom : list[float]) -> list[float]:

        for i in range(len(chromosom)):
            if chromosom[i] > self.max_vehicles:
                chromosom[i] = self.max_vehicles
    

    def get_initial_chromosoms(self, n : int) -> list[list[float]]:

        initials = []
        for i in range(n):
            initials.append([random.randint(1, self.max_vehicles) for j in range(len(self.edges))])
        
        return initials
   
    
    def get_default_chromosom(self) -> list[float]:

        avg_vehicles_nb = int(self.max_vehicles / 2)
        return [avg_vehicles_nb for i in range(len(self.edges))]


    def apply_chromosom(self, chromosom : list[float]):
        self.chromosom = chromosom


    def step_callback(*args):
        # si crossing == True ==> Checker si encoire vrai ==> 
        # Si crossing == false : 


        pass