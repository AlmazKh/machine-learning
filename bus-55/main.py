import requests
import pandas as pd
import time
import ast
import uuid
from math import sin, cos, sqrt, atan2, radians


def get_data():
    url = "http://data.kzn.ru:8082/api/v0/dynamic_datasets/bus.json"
    bus_number = "55"
    sleep_interval = 60.0

    with open("bus_data.txt", "a") as bus_list:
        while True:
            r = requests.get(url)
            print(r)
            data = pd.DataFrame(r.json())
            data = data["data"].to_dict()

            for i in data:
                if data[i]["Marsh"] == bus_number:
                    bus_list.write(str(data[i]) + "\n")
            time.sleep(sleep_interval)


def count_garages():
    garages = set()
    with open("bus_data.txt", "r") as bus_list:
        data = pd.DataFrame(bus_list)
        data = data.to_numpy()
        for line in data:
            line = ast.literal_eval(line[0])
            if line['GaragNumb'] not in garages:
                garages.add(line['GaragNumb'])
    return garages


class Station:
    def __init__(self, id_, name, lat=0.0, lon=0.0, next_station_id=None):
        self.id = id_
        self.name = name
        self.next_station_id = next_station_id
        self.lat = lat
        self.lon = lon


def reverse_graph(graph):
    return [Station(s.next_station_name, s.name) for s in graph][::-1]


# def generate_graph_without_lat_lon():
#    graph = []
#    # документ содержит уникальные имена остановок
#    with open("stations_uniq_names.txt", "r", encoding="utf-8") as stations:
#        lines = stations.readlines()
#        for i in range(len(lines) - 1):
#            graph.append(Station(lines[i][:lines[i].find('\n')], lines[i + 1][:lines[i + 1].find('\n')]))
#        # из-за особенностей маршрута приходит вручную удалять и добавлять некоторые остановки
#        graph.append(Station(lines[-1][:lines[-1].find('\n')], "Адоратского"))
#        reversed_graph = reverse_graph(graph)[13:]
#        reversed_graph[18] = Station(reversed_graph[18].name, reversed_graph[19].next_station_id)
#        reversed_graph.remove(reversed_graph[19])
#        graph += reversed_graph
#    return graph


def generate_graph():
    graph_ = list()
    with open("bus_stations.txt", "r", encoding="utf-8") as stations:
        lines = stations.readlines()
        for i in range(len(lines)):
            if graph_ == list():
                graph_.append(Station(i + 1, lines[i][:lines[i].find(' -')],
                                      float(lines[i][lines[i].find(', '): lines[i].find('\n')][2:]),
                                      float(lines[i][lines[i].find(' - '): lines[i].find(',')][3:])))
            elif i == len(lines) - 1:
                graph_.append(Station(i + 1, lines[i][:lines[i].find(' -')],
                                      float(lines[i][lines[i].find(', '): lines[i].find('\n')][2:]),
                                      float(lines[i][lines[i].find(' - '): lines[i].find(',')][3:]),
                                      graph_[0].id))
                graph_[0].next_station_id = i + 1
            else:
                graph_.append(Station(i + 1, lines[i][:lines[i].find(' -')],
                                      float(lines[i][lines[i].find(', '): lines[i].find('\n')][2:]),
                                      float(lines[i][lines[i].find(' - '): lines[i].find(',')][3:]),
                                      graph_[i - 1].id))
    return graph_


def get_station_by_id(graph_, id_):
    for item in graph_:
        if item.id == id_:
            return item


def calculate_distance(lat1, lon1, lat2, lon2):
    r = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c

    return distance


def bus_timer(garage, graph_):
    min_distance = 0.02  # 50 m
    with open("bus_data.txt", "r") as bus_list:
        data = pd.DataFrame(bus_list)
        data = data.to_numpy()
        with open("bus_timings_" + str(garage) + ".txt", "w", encoding='utf-8') as filtered_bus_list:
            for line in data:
                line = ast.literal_eval(line[0])
                if line["GaragNumb"] == str(garage):
                    lat, lon = float(line["Latitude"]), float((line["Longitude"]))
                    for station in graph_:
                        if calculate_distance(station.lat, station.lon, lat, lon) < min_distance:
                            filtered_bus_list.write(station.name + ' Time: ' + str(line['TimeNav']) + "\n")


get_data()
# [print(station.name) for station in generate_graph_without_lat_lon()]
# graph = generate_graph()
# вывод маршрута 55 автобуса
# [print(station.name, get_station_by_id(graph, station.next_station_id).name, sep=' -> ') for station in
# generate_graph()]

# print('Garages (different buses): ', *count_garages())
# для каждого автобуса сохраняем момент подъезда к остановке далее нужно будет для подсчета времени
# [bus_timer(garage, graph) for garage in count_garages()]
