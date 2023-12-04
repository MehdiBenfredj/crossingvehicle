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
        self.populations_and_fitness = {}
        self.srv = Service(config.sumo_folder, wkt.loads(self.params.polygons), self.params.intersection_ids)
        self.best_chromosomes = {}
        self.srv.generate_rou_file(self.params.duration, self.params.routes)
        for intersection_id in self.params.intersection_ids:
            self.populations_and_fitness[intersection_id] = self._generate_initial_pop(intersection_id)
        
        


    # Make sure the chromosom is valid (sum of phases = max_cycle_time)
    # If not, add or remove to a phase time randomly
    def _sanitize_chromosom(self, chromosom : list) -> list:

        indexes = [i for i in range(len(chromosom))]
        while sum(chromosom) != self.params.max_cycle_time:
            index = random.choices(indexes, k=1)[0]
            if sum(chromosom) > self.params.max_cycle_time:
                if chromosom[index] > self.params.min_phase_time:
                    chromosom[index] -= 1
            else:
                chromosom[index] += 1

        return chromosom


    def _generate_sanitized_chromosome(self) -> list[float]:
        chromosome = []
        for j in range(len(self.params.phases)):
            chromosome.append(random.randint(self.params.min_phase_time, self.params.max_cycle_time))
        return self._sanitize_chromosom(chromosome)


    def _generate_initial_pop(self, intersection_id : str) -> list[list[float]]:
        chromosoms = []
        for i in range(self.params.initial_pop_size):
            chromosome = self._generate_sanitized_chromosome()
            chromosoms.append([chromosome,self._compute_fitness(chromosome , intersection_id)])
        return chromosoms



    # Compute the fitness of a chromosom
    # The fitness is the average time spent by a vehicle in the area
    # The chromosom is applied to the intersection and the simulation is run
    # until there is no more vehicle in the area
    def _compute_fitness(self, chromosom : list, intersection_id : str) -> float:
        
        time_per_vehicle = {}
        conf_file_path = os.path.join(self.params.sumo_folder, self.params.sumo_cfg_file)
        if self.params.gui:
            traci.start(["sumo-gui", "-c", conf_file_path])
        else:
            traci.start(["sumo", "-c", conf_file_path])

        self.srv.apply_chromosom(intersection_id, chromosom, self.params.phases)
        for intersection_idd in self.params.intersection_ids:
            if intersection_idd != intersection_id:
                try :
                    self.srv.apply_chromosom(intersection_idd, self.best_chromosomes[intersection_idd], self.params.phases)
                except:
                    pass

        def1 = traci.trafficlight.getCompleteRedYellowGreenDefinition("J1")
        def2 = traci.trafficlight.getCompleteRedYellowGreenDefinition("J2")
        while traci.simulation.getMinExpectedNumber() > 0:
            
            vehicles_in_aera = self.srv.step(intersection_id)
            for vehicule in vehicles_in_aera:
                if vehicule in time_per_vehicle:
                    time_per_vehicle[vehicule] += 1
                else:
                    time_per_vehicle[vehicule] = 1
        
        traci.close()
        
        try :
            # s'il n'y a pas de vehicule dans la zone, on renvoie 10000
            return sum(time_per_vehicle.values())/len(time_per_vehicle)
        except:
            # 10000 est la valeur (théorique) maximale de fitness
            return 10000



    def _select_parents(self, intersection_id : str) -> list[list[float]]:
        sorted_pop = sorted(self.populations_and_fitness[intersection_id], key=lambda x: x[1])
        self.best_chromosomes[intersection_id] = sorted_pop[0][0]
        parents = [item[0] for item in sorted_pop[:self.params.parents_number]]
        return parents



    def _crossing(self, chromosom_a: list, chromosom_b: list) -> list[float]:
        parts = self.params.crossing_points + 1
        loc = int(len(chromosom_a) / parts)
        sub_lists_a = []
        sub_lists_b = []

        for i in range(parts):
            if i == parts - 1:
                sub_lists_a.append(chromosom_a[i * loc:])
                sub_lists_b.append(chromosom_b[i * loc:])
                continue
            sub_lists_a.append(chromosom_a[i * loc:(i + 1) * loc])
            sub_lists_b.append(chromosom_b[i * loc:(i + 1) * loc])

        chromosom_a = []
        chromosom_b = []
        for i in range(len(sub_lists_a)):
            if random.random() <= 0.5:
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

    def _update_populations(self):
        # parents dict (intersection_id : parents) 
        # select the best parents
        parents = {}
        for intersection_id in self.params.intersection_ids:
            parents[intersection_id] = self._select_parents(intersection_id)

        # children are also a dict (intersection_id : children[])
        children = { intersection_id : [] for intersection_id in self.params.intersection_ids }

        # crossing parents to generate children
        for intersection_id in self.params.intersection_ids:
            while len(children[intersection_id]) != self.params.children_number:
                couple = random.sample(parents[intersection_id], k=2)
                children[intersection_id].extend(self._crossing(couple[0], couple[1]))


        # mutation of children
        mutated_children = {}
        children_and_fitness = {}
        for intersection_id in self.params.intersection_ids:
            mutated_children[intersection_id] = [self._mutation(child) for child in children[intersection_id]]
            children_and_fitness[intersection_id] = [[child, self._compute_fitness(child, intersection_id)] for child in mutated_children[intersection_id]]
        
        # number of chromosomes to keep from the previous population
        keep_parents = self.params.initial_pop_size - self.params.children_number

        # sort the population by fitness
        sorted_populations = {}
        for intersection_id in self.params.intersection_ids:
            sorted_populations[intersection_id] = sorted(self.populations_and_fitness[intersection_id], key=lambda x: x[1])

        # keep the best chromosomes from the previous population
        # and make sure there is no duplicates
        new_populations = {}
        for intersection_id in self.params.intersection_ids:
            new_pop_fitnesses = []
            new_populations[intersection_id] = []
            for(index, item) in enumerate(sorted_populations[intersection_id]):
                if index < keep_parents and item[1] not in new_pop_fitnesses:
                    new_populations[intersection_id].append(item)
                    new_pop_fitnesses.append(item[1])

        # if there is not enough chromosomes, generate new ones
        for intersection_id in self.params.intersection_ids:
            number_of_new_chromosomes = keep_parents - len(new_populations[intersection_id])
            if(number_of_new_chromosomes != 0):
                for i in range(number_of_new_chromosomes):
                    chromosome = self._generate_sanitized_chromosome()
                    new_populations[intersection_id].append([chromosome, self._compute_fitness(chromosome, intersection_id)])

        # add the children to the new population
        for intersection_id in self.params.intersection_ids:
            new_populations[intersection_id].extend(children_and_fitness[intersection_id])
        
        # update the population
        self.populations_and_fitness = new_populations
        print("\"La nouvelle population est \" :")
        print(self.populations_and_fitness)
        print(",")



    def run(self) -> None:
        for i in range(self.params.iterations):
            self._update_populations()
        print("La meilleure solution est la suivante :")
        sorted_pop = sorted(self.populations_and_fitness, key=lambda x: x[1])
        print(sorted_pop[0][0])
        return(sorted_pop[0][1])

        
    def test_run(self) -> None:
        for i in range(1):
            self._update_populations()
        
        
