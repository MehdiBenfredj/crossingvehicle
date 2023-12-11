from roufilebuilder import Route
from intersections import TFIntersection, Intersection
import json
import csv
import os

class GeneticConfig():

    def __init__(self) -> None:

        # Sumo's configuration
        self.gui = False
        self.sumo_folder = "sumofiles"
        self.sumo_cfg_file = "conf.sumocfg"
        self.net_file = "unknown.net.xml"
        self.duration = 600

        # Genetic algorithm's configuration
        self.iterations = 100
        self.parents_number = 4
        self.children_number = 4
        self.crossing_points = 1
        self.crossing_mode = "classic"
        self.mutation_proba = 0.5
        self.initial_pop_size = 8

        # Output CSV file
        self.output_file = ""

        # Intersections and routes
        self.intersections = []
        self.routes = []


    def load_from_file(self, file : str = "config.json"):
        with open(file, 'r') as json_file:
            values = json.load(json_file)

        # Sumo configuration 
        self.gui = values["gui"]
        self.sumo_folder = values["sumo_folder"]
        self.sumo_cfg_file = values["sumo_cfg_file"]
        self.net_file = values["net_file"]
        self.duration = values["duration"]

        # Genetic algorithm's configuration
        self.iterations = values["iterations"]
        self.parents_number = values["parents_number"]
        self.children_number = values["children_number"]
        self.crossing_points = values["crossing_points"]
        self.crossing_mode = values["crossing_mode"]
        self.mutation_proba = values["mutation_proba"]
        self.initial_pop_size = values["initial_pop_size"]

        # Intersections and routes
        self.intersections = [self._load_intersection(inter) for inter in values["intersections"]]
        self.routes = [self._load_route(rou) for rou in values["routes"]]


    def set_output_file_and_mkdirs(self, fp : str):

        if os.path.dirname(fp) != "":
            os.makedirs(os.path.dirname(fp), exist_ok=True)
        self.output_file = fp
        with open(self.output_file, "w") as csv_file:
            writer = csv.writer(csv_file)
            


    def _load_route(self, route : dict) -> Route:
        return Route(route["label"], route["vehicles"], route["edges"])


    def _load_intersection(self, inter : dict) -> Intersection:
        
        if inter["kind"] == "tf":
            return TFIntersection(
                inter["id"],
                inter["center"],
                inter["visibility"],
                inter["id"],
                inter["phases"],
                inter["min_phase_time"],
                inter["cycle_time"]
            )
        
        # Others intersections...
        