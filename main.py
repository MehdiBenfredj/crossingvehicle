import libsumo as traci
from service import Service

# Créer un Service
srv = Service("sumofiles")

# Générer le rou file
srv.generate_rou_file()

# Lancer sumo avec python
traci.start(["sumo-gui", "-c", "sumofiles/config.sumocfg"])

srv.apply_chromosom("J1", (3,3,3,3))
print(traci.trafficlight.getCompleteRedYellowGreenDefinition("J1"))