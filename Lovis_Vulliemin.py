# -coding: UTF-8
import pygame

from voyager import Voyager
from city import City
from gui import Gui

def ga_solve(file=None, gui=True, maxtime=0):
    distance = 0

    cities = []
    if file is not None:
        cities = use_file(file)
    #Data acquisition
    if(gui):
        use_gui(cities)

    #TODO algo genetic

    #TODO get distance

    # Return total distance
    return distance


def use_gui(cities):
    gui = Gui()
    gui.show(cities)

def use_file(path):
    cities = []

    with open(path) as f:
        content = f.readlines()

    for c in [x.strip() for x in content]:
        tmp_values = c.split()
        cities.append(City(tmp_values[0], tmp_values[1], tmp_values[2]))

    print("Readed datas :")
    for city in cities:
        print(city)
    return cities

if __name__ == '__main__':
	ga_solve("data\pb005.txt", False, 100)

