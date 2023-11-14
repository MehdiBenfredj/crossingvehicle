from roufilebuilder import *
from shapely import Polygon, Point
import libsumo as traci
import random as rd
import os

class Service():
    def __init__(self, sumo_folder : str) -> None:
        self.path = os.path.abspath(sumo_folder)
        os.makedirs(self.path, exist_ok=True)

    def get_all_vehicles_and_pos(self) -> list[tuple]:
        id_pos = []
        ids = traci.vehicle.getIDList()
        for id in ids:
            pos = traci.vehicle.getPosition(id)
            id_pos.append((id,pos))

    def get_vehicle_in_area(self, area : Polygon) -> list[str]:
        vehicles_in_area = []
        vehicles = self.get_all_vehicles_and_pos()
        for vehicle in vehicles:
            point = Point(vehicle[1][0], [1][1])
            if area.contains(point):
                vehicles_in_area.append(vehicle[0])
        return vehicles_in_area


    def apply_chromosom(self, chromosom : list):
        


    def generate_rou_file(self):
        rou_file = RouFile()

        # Définition d'un type de véhicule (voiture)
        rou_file.insert(new_vehicle_type("car",1.0,5.0,4.0,2.5,50.0,0.5,"passenger"))

        # Définition des trajets
        rou_file.insert(new_route("trajetNS",["E0","E1"])) # Nord vers Sud
        rou_file.insert(new_route("trajetSN",["-E1","-E0"])) # Sud vers Nord
        rou_file.insert(new_route("trajetEW",["-E3","-E2"])) # Est vers Ouest
        rou_file.insert(new_route("trajetWE",["E2","E3"])) # Ouest vers Est

        for i in range(25):
            rou_file.insert(new_vehicle("veh{}".format(i), "trajetNS", "car", rd.randint(1000,10000), (1,0,0)))
        # Save file
        rou_file.save(self.path)