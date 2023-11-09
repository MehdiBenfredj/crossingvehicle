from roufilebuilder import *
from shapely import Polygon, Point
import libsumo as traci
import os

class Service():
    def __init__(self, sumo_file_folder : str) -> None:
        self.path = os.path.abspath(sumo_file_folder)
        os.makedirs(self.path, exist_ok=True)

    def get_all_vehicles_and_pos(self) -> list[tuple]:
        id_pos = []
        ids = traci.vehicle.getIDList()
        for id in ids:
            pos = traci.vehicle.getPosition(id)
            id_pos.append((id,pos))

    def get_vehicle_in_aera(self, aera : Polygon) -> list[str]:
        vehicles_in_aera = []
        vehicles = self.get_all_vehicles_and_pos()
        for vehicle in vehicles:
            point = Point(vehicle[1][0], [1][1])
            if aera.contains(point):
                vehicles_in_aera.append(vehicle[0])

    def apply_chromosom(self, chromosom : tuple):
        pass


