<<<<<<< .mine
# -coding: UTF-8
import pygame
=======
from city import City

>>>>>>> .theirs

class Ville(object):

    def __init__(self):
        self.x = 0
        self.y = 0


def ga_solve(file=None, gui=True, maxtime=0):
    distance = 0

    #Data acquisition
    if(gui):
        use_gui()
    else:
        use_file(file)

    #TODO algo genetic

    #TODO get distance

    # Return total distance
    return distance


def use_gui():
    pass
<<<<<<< .mine















=======

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

>>>>>>> .theirs
if __name__ == '__main__':
<<<<<<< .mine
    print("main")
=======
	ga_solve("data\pb005.txt", False, 100)
>>>>>>> .theirs
