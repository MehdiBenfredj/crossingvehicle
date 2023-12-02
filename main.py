from algcfg import GeneticConfig
from genetic import GeneticAlgorithm

from service import Service
from shapely import Polygon
import os

conf = GeneticConfig()
conf.load_from_file(os.getenv("ALGCONF","configtriple.json"))

alg = GeneticAlgorithm(conf)


alg.run()


####
#Test changes
#fitnesses = []
#for i in range(10):
#	fitnesses.append(alg.run())
#print(sum(fitnesses)/10)
####