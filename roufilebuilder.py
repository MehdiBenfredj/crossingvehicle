import os


def new_route(id : str, edges : list) -> str:
    edge_str = ""
    for edge in edges:
        edge_str = edge_str + str(edge) + " "
    return "\t<route id=\"{}\" edges=\"{}\">".format(id, edge_str)
    
def new_vehicle_type(id : str, accel : float, decel : float, length : float , minGap : float, maxSpeed : float, sigma : float, gui_shape : str) -> str:
    return "\t<vType id=\"{}\" accel=\"{}\" decel=\"{}\" length=\"{}\" minGap=\"{}\" maxSpeed=\"{}\" sigma=\"{}\">".format(id, accel,
            decel, length, minGap, maxSpeed, sigma, gui_shape)
    
def new_vehicle(id : str, route_id : str, type_id : str, depart : int, color_rgb : tuple = (1,1,1)):
    color_str = "{},{},{}".format(color_rgb[0], color_rgb[1], color_rgb[2])
    return "\t<vehicle depart=\"{}\" id=\"{}\" route=\"{}\" type=\"{}\" color=\"{}\">".format(depart, id, route_id, type_id, color_str)
    

class RouFile():
    def __init__(self) -> None:
        self.rows = ["<?xml version=\"1.0\" encoding=\"UTF-8\">",
                     "<routes>"]
        
    def insert(self, balise : str) -> None:
        self.rows.append(balise)

    def save(self, folder : str, name : str = "generated.rou.xml"):
        self.rows.append("</routes>")
        with open(os.path.join(folder, name),"w") as rou_file:
            for row in self.rows:
                rou_file.write(row + "\n")