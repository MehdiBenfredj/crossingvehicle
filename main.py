import libsumo as traci
from service import Service
from shapely import Polygon

coords = ((0,0),(0,1),(1,1),(1,0),(0,0))

# Créer un Service
srv = Service("sumofiles", Polygon(coords))

# Générer le rou file
srv.generate_rou_file(600, [20, 20, 20, 20])

# Lancer sumo avec python
traci.start(["sumo-gui", "-c", "sumofiles/config.sumocfg"])

srv.apply_chromosom("J1", (3,3,3,3))
print(traci.trafficlight.getCompleteRedYellowGreenDefinition("J1"))
