# -coding: UTF-8
import pygame
import datetime

from voyager import Voyager
from city import City
from gui import Gui

def ga_solve(file=None, gui=True, maxtime=5):
    distance = 0
    cities = []

    #Data acquisition
    if file is not None:
        cities = use_file(file)

    if(gui):
        use_gui(cities)

    voyager = Voyager(cities)       #This is the problem holder
    print("Generation 0 :\n" + str(voyager))

    #Genetical algo
    i = 1
    begin_time = datetime.datetime.now()
    elapsed_time = 0

    while(elapsed_time < maxtime):
        print("Generation "+str(i)+" :\n" +str(voyager))

        voyager.apply_genetical()

        elapsed_time = datetime.datetime.now().second - begin_time.second
        print("Elapsed time :" + str(elapsed_time)+"\n")

        i += 1


    #TODO get best distance and return
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
	ga_solve("data\pb005.txt", False, 5)

