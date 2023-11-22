from dotenv import dotenv_values

class GeneticConfig():
    def __init__(self) -> None:
        self.gui = None
        self.sumo_folder = None
        self.sumo_cfg_file = None
        self.iterations = None
        self.intersection_id = None
        self.min_phase_time = None
        self.max_cycle_time = None
        self.parents_number = None
        self.children_number = None
        self.crossing_points = None
        self.mutation_proba = None
        self.initial_pop_size = None
        # other params...


    def is_valid(self) -> bool:
        return None not in list(vars(self).values)
    
    
    def print_undefined_items(self):
        print("Unable to run algorithm (Bad configuration) :")
        for k, value in vars(self).items():
            if value == None:
                print("- {} undefined".format(k))
                

    def load_from_env_file(self, file : str = "env"):
        try:
            values = dotenv_values()
            self.gui = values["GUI"].lower() in ["true", "t", "1", "yes", "y"]
            self.sumo_folder = values["SUMO_FOLDER"]
            self.sumo_cfg_file = values["SUMO_CFG_FILE"]
            self.iterations = values["ITERATIONS"]
            self.intersection_id = values["INTERSECTION_ID"]
            self.min_phase_time = values["MIN_PHASE_TIME"]
            self.max_cycle_time = values["MAX_CYCLE_TIME"]
            self.parents_number = values["PARENTS_NUMBER"]
            self.children_number = values["CHILDREN_NUMBER"]
            self.crossing_points = values["CROSSING_POINTS"]
            self.mutation_proba = values["MUTATION_PROBA"]
            self.initial_pop_size = values["INITIAL_POP_SIZE"]
        except:
            pass