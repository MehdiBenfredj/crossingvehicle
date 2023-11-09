from service import Service
import libsumo

class GeneticAlgorithm():
    def __init__(self, service : Service, gui_active : bool) -> None:
        self.srv = service
        self.gui = gui_active
        self.folder

    def run(self):
        if self.gui:
            libsumo.start(["sumo-gui", "-c", "file.sumocfg"])
        else:
            libsumo.start(["sumo", "-c", "file.sumocfg"])