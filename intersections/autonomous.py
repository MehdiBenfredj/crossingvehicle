from intersections.intersection import Intersection
import random
import sumolib

class AutoIntersection(Intersection):

    def __init__(self, id: str, center: list[float], visibility: float, edges_id: list[str], edges_len: list[float]) -> None:
        super().__init__(id, center, visibility)

        self.edges_id = edges_id
        self. edges_len = edges_len
        self.crossing = False
        self.chromosom = []
        self.priorities = []
        self.carousel = Carousel()
        

    
    def _get_edges_id_and_len(self, net_path: str) -> list[str]:

        edges = sumolib.net.readNet(net_path).getEdges()
        edges_id=[]
        edges_len=[]

        for edge in edges:
            if edge.getToNode().getID() == self.id :
                edges_id.append(edge.getID())
                edges_len.append(edge.getLength())

        return edges_id, edges_len


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
        self.carousel.set_max_vehicles(chromosom)


    def step_callback(*args):
        # si crossing == True ==> Checker si encoire vrai ==> 
        # Si crossing == false : 
        pass



class Carousel():
    def __init__(self,edges:list[str], len_edge:list[float]):
        self.cursor = random.randint(0,len(edges)-1)
        self.edges = edges
        self.len_edge = len_edge
        self.max_vehicles = []
        self.crossing = False
        self.ignore_vehicles = [] #the vehicles that will cross the intersection
    
    #set stop for the lanes
    def _maintain_stop(self):
        pass

    #renvoyer la liste des vehicules sur une voie en ordre de plus proche au plus loin
    def _get_veh_on_selected_lane(self):
        pass
    
    #les vehicules qui doivent passer
    def _get_veh_tocross(self):
        pass

    #changer de voie
    def _switch_lane(self):
        pass

    def _update_lane_priorities(self):
        pass

    #verifier s'il y'a des vehicules qui circulent dans l'intersection
    def _verify_crossing(self):
        pass

    def set_max_vehicles(self, value:list[float]):
        self.max_vehicles = value

    def step():
        pass