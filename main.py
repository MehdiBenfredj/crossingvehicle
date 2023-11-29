from algcfg import GeneticConfig
from genetic import GeneticAlgorithm

from service import Service
from shapely import Polygon
import os

conf = GeneticConfig()
conf.load_from_file(os.getenv("ALGCONF","config.json"))

alg = GeneticAlgorithm(conf)
alg.run()
