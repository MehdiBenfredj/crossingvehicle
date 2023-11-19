from roufilebuilder import *
from shapely import Polygon, Point
import libsumo as traci
import random as rd
import os


class Service():

    def __init__(self, sumo_folder : str, area : Polygon) -> None:
        self.path = os.path.abspath(sumo_folder)
        self.area = area
        os.makedirs(self.path, exist_ok=True)


    def __get_all_vehicles_and_pos(self) -> list[tuple]:
        id_pos = []
        ids = traci.vehicle.getIDList()
        for id in ids:
            pos = traci.vehicle.getPosition(id)
            id_pos.append((id,pos))


    def _get_vehicle_in_area(self) -> list[str]:
        vehicles_in_area = []
        vehicles = self.__get_all_vehicles_and_pos()
        for vehicle in vehicles:
            point = Point(vehicle[1][0], [1][1])
            if self.area.contains(point):
                vehicles_in_area.append(vehicle[0])
        return vehicles_in_area


    def apply_chromosom(self, intersection_id : str, chromosom : tuple):

        phases = [
            traci.TraCIPhase(chromosom[0], "GrGr", 0, 0),
            traci.TraCIPhase(chromosom[1], "yryr", 0, 0),
            traci.TraCIPhase(chromosom[2], "rGrG", 0, 0),
            traci.TraCIPhase(chromosom[3], "ryry", 0, 0)
        ]

        logic = traci.TraCILogic("custom", "static", 0, phases)
        traci.trafficlight.setProgramLogic(intersection_id, logic)


    def step(self) -> list[str]:
        traci.simulationStep()
        return self._get_vehicle_in_area()


    def generate_rou_file(self):

        rou_file = RouFile()

        # Vehicle type definition
        rou_file.new_vehicle_type("car",1.0,5.0,4.0,2.5,50.0,0.5,"passenger")

        # Routes definition
        routes = ["trajetNS", "trajetSN", "trajetEW", "trajetWE"]
        rou_file.new_route(routes[0],["E0","E1"]) # Nord vers Sud
        rou_file.new_route(routes[1],["-E1","-E0"]) # Sud vers Nord
        rou_file.new_route(routes[2],["-E3","-E2"]) # Est vers Ouest
        rou_file.new_route(routes[3],["E2","E3"]) # Ouest vers Est

        # Generate 25 vehicules with random depart on each route
        for route in routes:
            for i in range(25):
                rou_file.new_vehicle("veh{}".format(i), route, "car", rd.randint(1000,10000), (1,0,0))
            

        # Save file
        rou_file.save(self.path)
