import codecs
import pandas as pd
import ast
from math import sin, cos, sqrt, atan2, radians


class LatLon:
    lat = 0.0
    lon = 0.0

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


bus_stations_dict = {}
min_distance_km = 0.01


def calc_distance(latLon1, latLon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(latLon1.lat)
    lon1 = radians(latLon1.lon)
    lat2 = radians(latLon2.lat)
    lon2 = radians(latLon2.lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


with codecs.open("bus_stations.txt", "r", "utf-8") as bus_stations_txt:
    for line in bus_stations_txt.readlines():
        name = line[line.find("-") + 1:line.find("\r")]
        bus_stations_dict[name] = LatLon(float(line[:line.find("-")][:line.find(",")]),
                                         float(line[:line.find("-")][line.find(",") + 1:]))

print(bus_stations_dict)

with open("bus_data.txt", "r") as bus_list:
    data = pd.DataFrame(bus_list)
    data = data.to_numpy()
    for line in data:
        line = ast.literal_eval(line[0])
        busLatLon = LatLon(float(line["Latitude"]), float((line["Longitude"])))
        for key in bus_stations_dict.keys():
            if calc_distance(bus_stations_dict[key], busLatLon) < min_distance_km:
                with open("filtered_bus_list.txt", "a") as filtered_bus_list:
                    filtered_bus_list.write(str(line) + "\n")
