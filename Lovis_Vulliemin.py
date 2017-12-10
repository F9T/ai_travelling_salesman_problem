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
        cities = load_file(file)

    if gui:
        gui = Gui()
        gui.show(cities)

    voyager = Voyager(cities)       #This is the problem holder
    print("Generation 0 :\n" + str(voyager))

    #Genetical algo
    i = 1
    begin_time = datetime.datetime.now()
    elapsed_time = 0

    while(elapsed_time < maxtime and elapsed_time >= 0):
        print("Generation "+str(i)+" :\n" +str(voyager))

        #Apply genetical algo
        voyager.apply_genetical()

        #Show on pygame
        if gui:
            gui.draw_cities(voyager.best_solution.path_cities, True)

        #Just calculate and print the time elapsed
        elapsed_time = datetime.datetime.now().second - begin_time.second
        print("Elapsed time :" + str(elapsed_time)+"\n")

        i += 1

    if gui:
        gui.wait()

    return distance


def use_gui(cities):
    gui = Gui()
    gui.show(cities)

def load_file(path):
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
	ga_solve("data\pb010.txt", True, 5)