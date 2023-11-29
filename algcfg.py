import json

class GeneticConfig():
    def __init__(self) -> None:
        self.duration = None
        self.phases = []
        self.routes = []
        self.gui = None
        self.sumo_folder = None
        self.sumo_cfg_file = None
        self.iterations = None
        self.intersection_id = None
        self.polygon = None
        self.min_phase_time = None
        self.max_cycle_time = None
        self.parents_number = None
        self.children_number = None
        self.crossing_points = None
        self.mutation_proba = None
        self.initial_pop_size = None
        # other params...



    def load_from_file(self, file : str = "config.json"):
        with open(file, 'r') as json_file:
            values = json.load(json_file)

        self.duration = values["duration"]
        self.phases = values["phases"]
        self.routes = values["routes"]
        self.gui = values["gui"]
        self.sumo_folder = values["sumo_folder"]
        self.sumo_cfg_file = values["sumo_cfg_file"]
        self.iterations = values["iterations"]
        self.intersection_id = values["intersection_id"]
        self.polygon = values["polygon"]
        self.min_phase_time = values["min_phase_time"]
        self.max_cycle_time = values["max_cycle_time"]
        self.parents_number = values["parents_number"]
        self.children_number = values["children_number"]
        self.crossing_points = values["crossing_points"]
        self.mutation_proba = values["mutation_proba"]
        self.initial_pop_size = values["initial_pop_size"]
        # set other params