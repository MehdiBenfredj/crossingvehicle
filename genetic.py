from service import Service
import libsumo
import os

class GeneticAlgorithm():
    def __init__(self, service : Service, gui_active : bool, sumo_folder : str, sumo_cfg_file : str) -> None:
        self.srv = service
        self.gui = gui_active
        self.sumo_folder = sumo_folder
        self.sumo_cfg = sumo_cfg_file

    def run(self):
        conf_file_path = os.path.join(self.sumo_folder, self.sumo_cfg)
        if self.gui:
            libsumo.start(["sumo-gui", "-c", conf_file_path])
        else:
            libsumo.start(["sumo", "-c", conf_file_path])