from service import Service
import numpy as np
import libsumo as traci
import os

class GeneticAlgorithm():

    def __init__(self, gui_active : bool, sumo_folder : str, sumo_cfg_file : str) -> None:
        self.gui = gui_active
        self.sumo_folder = sumo_folder
        self.sumo_cfg = sumo_cfg_file

        self.population = []
        self.fitness = []
        
        self.srv = Service(sumo_folder)

    def generate_initial_pop(self, max_cycle_time : int):
        pass
    
    def _compute_fitness(self, chromosom : tuple) -> float:
        
        time_per_vehicle = {}
         
        conf_file_path = os.path.join(self.sumo_folder, self.sumo_cfg)
        if self.gui:
            traci.start(["sumo-gui", "-c", conf_file_path])
        else:
            traci.start(["sumo", "-c", conf_file_path])

        self.srv.apply_chromosom("J0", chromosom)
        while traci.simulation.getMinExpectedNumber() > 0:
            
            vehicles_in_aera = self.srv.step()
            for vehicule in vehicles_in_aera:
                if vehicule in time_per_vehicle:
                    time_per_vehicle[vehicule] += 1
                else:
                    time_per_vehicle[vehicule] = 1
        
        traci.close()

        return sum(time_per_vehicle.values())/len(time_per_vehicle)



    def _select_parents(self) -> list[list[float]]:
        pass


    def _crossing(self, chromosom_a : list, chromosom_b : list, nb_points : int = 1) -> list[float]:
        parts = nb_points+1
        loc = int(len(chromosom_a)/parts)
        sub_lists_a = []
        sub_lists_b = []

        for i in range(parts):
            if i == parts-1:
                sub_lists_a.append(chromosom_a[i*loc:])
                sub_lists_b.append(chromosom_b[i*loc:])
                continue
            sub_lists_a.append(chromosom_a[i*loc:(i+1)*loc])
            sub_lists_b.append(chromosom_b[i*loc:(i+1)*loc])


        
    def run(self, iterations : int) -> None:
        self.srv.generate_rou_file()
        for item in self.population:
            self.fitness.append(self._compute_fitness(item))

        

        
