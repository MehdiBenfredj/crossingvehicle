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

        time_per_vehicle = []

        conf_file_path = os.path.join(self.sumo_folder, self.sumo_cfg)
        if self.gui:
            traci.start(["sumo-gui", "-c", conf_file_path])
        else:
            traci.start(["sumo", "-c", conf_file_path])

        self.srv.apply_chromosom("J0", chromosom)
        while traci.simulation.getMinExpectedNumber() > 0:
            
            # Compute fitness
            vehicles_in_aera = self.srv.step()
            # Compute
        
        traci.close()
        
        # Compute fitness
        fitness = []

        return fitness

        



    def _select_parents(self) -> list[list[float]]:
        pass

    def _crossing(self) -> list[float]:
        pass
        
    def run(self, iterations : int) -> None:
        self.srv.generate_rou_file()
        for item in self.population:
            self.fitness.append(self._compute_fitness(item))

        

        
