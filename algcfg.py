from dotenv import dotenv_values

class GeneticConfig():
    def __init__(self) -> None:
        self.gui = "hello"
        self.sumo_folder = "world"
        self.sumo_cfg_file = 6
        self.min_phase_time = 6
        self.max_cycle_time = 6
        # other params...


    def is_valid(self) -> bool:
        return None not in list(vars(self).values)
    
    
    def print_undefined_items(self):
        print("Unable to run algorithm (Bad config) :")
        for k, value in vars(self).items():
            if value == None:
                print("- {} undefined")
                

    def load_from_env_file(self, file : str = "env"):
        try:
            values = dotenv_values()
            self.gui = values["GUI"].lower() in ["true", "t", "1", "yes"]
            self.sumo_folder = values["SUMO_FOLDER"]
            self.sumo_cfg_file = values["SUMO_CFG_FILE"]
            self.min_phase_time = values["MIN_PHASE_TIME"]
            self.max_cycle_time = values["MAX_CYCLE_TIME"]
        except:
            pass