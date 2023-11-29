from service import Service
from algcfg import GeneticConfig
from shapely import wkt
import random
import libsumo as traci
import os

# TODO : reduire les appels à sorted

class GeneticAlgorithm():

    def __init__(self, config : GeneticConfig) -> None:
        self.params = config
        self.srv = Service(config.sumo_folder, wkt.loads(self.params.polygon))
        self.srv.generate_rou_file(self.params.duration, self.params.routes) 
        self.population_and_fitness = self._generate_initial_pop()
        


    def _sanitize_chromosom(self, chromosom : list) -> list:

        indexes = [i for i in range(len(chromosom))]
        while sum(chromosom) != self.params.max_cycle_time:
            index = random.choices(indexes, weights=chromosom, k=1)[0]
            if sum(chromosom) > self.params.max_cycle_time:
                if chromosom[index] > self.params.min_phase_time:
                    chromosom[index] -= 1
            else:
                chromosom[index] += 1

        return chromosom


    def _generate_initial_pop(self) -> list[list[float]]:
        chromosoms = []
        for i in range(self.params.initial_pop_size):
            chromosom = []
            for j in range(len(self.params.phases)):
                chromosom.append(random.randint(self.params.min_phase_time, self.params.max_cycle_time))
            chromosom = self._sanitize_chromosom(chromosom)
            chromosoms.append([chromosom,self._compute_fitness(chromosom)])
        return chromosoms

    

    def _compute_fitness(self, chromosom : list) -> float:
        
        time_per_vehicle = {}
        conf_file_path = os.path.join(self.params.sumo_folder, self.params.sumo_cfg_file)
        if self.params.gui:
            traci.start(["sumo-gui", "-c", conf_file_path])
        else:
            traci.start(["sumo", "-c", conf_file_path])

        self.srv.apply_chromosom(self.params.intersection_id, chromosom, self.params.phases)
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
        
        sorted_pop = sorted(self.population_and_fitness, key=lambda x: x[1])
        parents = [item[0] for item in sorted_pop[:self.params.parents_number]]
        return parents



    def _crossing(self, chromosom_a : list, chromosom_b : list) -> list[float]:

        parts = self.params.crossing_points+1
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

        chromosom_a = []
        chromosom_b = []
        for i in range(len(sub_lists_a)):
            if i%2 == 0:
                chromosom_a.extend(sub_lists_a[i])
                chromosom_b.extend(sub_lists_b[i])
            else:
                chromosom_a.extend(sub_lists_b[i])
                chromosom_b.extend(sub_lists_a[i])
        
        return [chromosom_a, chromosom_b]



    def _mutation(self, chromosom : list) -> list:

        rand_number = random.random()
        if rand_number < self.params.mutation_proba:
            rand_index = random.randint(0, len(chromosom)-1)
            rand_modif = random.randint(1,3)
            rand_number = random.random()
            if rand_number <= 0.5:
                if chromosom[rand_index] - rand_modif >= self.params.min_phase_time:
                    chromosom[rand_index] -= rand_modif
            else:
                chromosom[rand_index] += rand_modif
        
            return self._sanitize_chromosom(chromosom)
        return chromosom



    def _update_pop(self):

        parents = self._select_parents()
        children = []

        while len(children) != self.params.children_number:
            couple = random.choices(parents, k=2)
            children.extend(self._crossing(couple[0], couple[1]))

        mutated_children = [self._mutation(child) for child in children]
        children_and_fitness = [[child, self._compute_fitness(child)] for child in mutated_children]
        
        keep_parents = len(self.population_and_fitness) - self.params.children_number
        new_pop = sorted(self.population_and_fitness, key=lambda x: x[1])[:keep_parents]
        new_pop.extend(children_and_fitness)
        
        self.population_and_fitness = new_pop
        print("La nouvelle population est :")
        print(self.population_and_fitness)



    def run(self) -> None:
        for i in range(self.params.iterations):
            self._update_pop()
        print("La meilleure solution est la suivante :")
        sorted_pop = sorted(self.population_and_fitness, key=lambda x: x[1])
        print(sorted_pop[0][0])

        

        
