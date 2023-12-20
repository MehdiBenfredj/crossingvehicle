from algcfg import GeneticConfig
import libsumo as traci
import time
import sys
import os

try:
    conf_file = sys.argv[1]
except:
    print("==> You must pass a configuration file as argument")

conf = GeneticConfig()
conf.load_from_file(conf_file)

chromosoms = []
for inter in conf.intersections:
    print("==> Enter chromosom for intersection", inter.id, "(type :", type(inter).__name__, ")")
    csv_chrom = str(input())
    splited_chrom = csv_chrom.split(",")
    chromosoms.append([int(value) for value in splited_chrom])

sumo_cfg = os.path.join(conf.sumo_folder, conf.sumo_cfg_file)
traci.start(["sumo-gui", "-c", sumo_cfg])

for i in range(len(conf.intersections)):
    conf.intersections[i].apply_chromosom(chromosoms[i])

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() 
    for j in range(len(conf.intersections)):
        conf.intersections[j].step_callback()
    time.sleep(1)



