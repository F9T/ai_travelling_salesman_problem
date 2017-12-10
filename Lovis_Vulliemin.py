# -coding: UTF-8
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
import datetime
from math import pow, sqrt
import sys
from city import City
import random
import functools
from copy import deepcopy

STAGNATION_TOLERANCE = 100
MAX_TIME_ELAPSED = 10
POPULATION_SIZE = 100
MUTATION_RATE = 0.4


class Gui(object):

    def __init__(self, width=500, height=500, city_color=[10, 10, 200], city_radius=3, line_color=[250, 50, 50]):
        self.width = width
        self.height = height
        self.window = None
        self.screen = None
        pygame.init()
        pygame.display.set_caption('Problème du voyageur de commerce')
        self.font = pygame.font.Font(None, 30)
        self.city_color = city_color
        self.line_color = line_color
        self.city_radius = city_radius
        self.font_color = [255, 255, 255]

    def show(self, cities=[]):
        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.get_surface()
        self.collection_cities(cities)

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    pygame.display.flip()

    def collection_cities(self, cities):
        collecting = True
        self.draw_cities(cities)

        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    city = City("v"+str(len(cities)), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    cities.append(city)
                    self.draw_cities(cities)

                self.screen.fill(0)
        pygame.display.flip()

    #Draw for beggining and entering cities with GUI
    def draw_cities(self, cities, draw_path=False):
        self.screen.fill(0)

        #Show Number of city text
        text = self.font.render("Nombre: %i" % len(cities), True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)

        #Compute for path show
        if draw_path:
            list_points = []

        #Show cities points
        for city in cities:
            pygame.draw.circle(self.screen, self.city_color, (city.x, city.y), self.city_radius)

            if draw_path:
                list_points.append((city.x, city.y))

        if draw_path:
            pygame.draw.lines(self.window, self.line_color, False, list_points, 1)

        pygame.display.flip()


class City:

    def __init__(self, id, x, y):
        self.id = id
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        text = ', '.join("%s: %s" % item for item in vars(self).items()) #https://stackoverflow.com/questions/5969806/print-all-properties-of-a-python-class
        return str(text)

    def __eq__(self, other):
        return self.id == other.id


class Solution:
    def __init__(self, path_cities):
        self.path_cities = path_cities
        self.calculate_distance()
        #self.coupled = False

    def __getitem__(self, item):
        return self.path_cities[item]

    def __setitem__(self, key, value):
        self.path_cities[key] = value

    def __str__(self):
        text = "Solution : ["
        for city in self.path_cities:
            if city.id is not None:
                text += city.id +" "
        text += "] Distance : " + str(self.total_distance)
        return str(text)

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self, other):
        pass    #TODO greater and lesser to compare for max

    def mutate(self):
        #Swap 2 values
        rands = random.sample(range(len(self.path_cities)), 2)#Check if 0-4

        self[rands[0]], self[rands[1]] = self[rands[1]], self[rands[0]]
        self.calculate_distance()

    def calculate_difference(self, other):
        differences = 0
        for i in range(len(self.path_cities)):
            if self.path_cities[i] == other.path_cities[i]:
                differences += 1
        return differences

    # sqrt((x2-x1)^2+(y2-y1)^2) between each cities
    def calculate_distance(self):
        self.total_distance = 0
        for i in range(len(self.path_cities) - 1):   #-1 => Cause we use i and i+1
            self.total_distance += sqrt(pow(self.path_cities[i+1].x - self.path_cities[i].x, 2) + pow(self.path_cities[i+1].y - self.path_cities[i].y, 2))



class Voyager:
    def __init__(self, cities):
        self.problem = cities  # Contains all cities unordered
        self.solutions = []  # Contains all solution (path that visit all cities 1 time)

        #Populate
        self.solutions.append(Solution(cities))  # Affect first order and reverse order to solutions
        self.solutions.append(Solution(list(reversed(cities))))
        for i in range(POPULATION_SIZE-2):
            self.solutions.append(Solution(sorted(cities, key=lambda k: random.random())))

        self.best_solution = self.solutions[0]  # Contains the current best solution
        self.find_best_solution()

    def __str__(self, debug=True):
        text = "Voyager :"
        if debug:
            text += "\n"
            for solution in self.solutions:
                text += str(solution) + "\n"
        text += "\nBest is : " + str(self.best_solution)
        return str(text)

    def __eq__(self, other):
        return self.id == other.id

    def apply_genetical(self):
        self.select_solutions()
        self.cross_over_solutions()
        self.mutate_solutions()
        self.find_best_solution()#May be externalized

    def select_solutions(self):
        #Calculate median solutions distance
        distances = (sol.total_distance for sol in self.solutions)
        median = functools.reduce(lambda a, b: a + b, distances)/POPULATION_SIZE

        #Select parents
        selecteds = [solution for solution in self.solutions if solution.total_distance < median]

        #Select other random to complete half of the population
        while(len(selecteds) < len(self.solutions)/2):
            selecteds.append(self.solutions[random.randint(0, len(self.solutions)-1)])

        self.solutions = selecteds

    def cross_over_solutions(self):
        while len(self.solutions) < POPULATION_SIZE:
            # Choose parents and form couples
            couple = random.sample(self.solutions, 2)

            # Choose segment points
            segment_points = (random.sample(range(len(self.problem) + 1), 2))
            segment_points.sort()

            # Create child based on 1st parent
            child = deepcopy(couple[0])

            # Replace inner segments cities
            missings = []
            for i in range(segment_points[0], segment_points[1]):
                # check if doubled cities outter of segment_points
                if couple[1][i] in child[:segment_points[0]] or couple[1][i] in child[segment_points[1]:]:
                    pos_double = child.path_cities.index(couple[1][i])
                    missings.append(child[pos_double])
                    child[pos_double] = City(-1, 0, 0)

                child[i] = couple[1][i]  # Place 2nd parent value

            # for i in range(segment_points[0])+range(segment_points[1], len(child.path_cities)):
            for x in (i for j in (range(segment_points[0]), range(segment_points[1], len(child.path_cities))) for i in
                      j):
                if child[i].id == -1:
                    child[i] = missings.pop()

            self.solutions.append(child)

    def mutate_solutions(self):
        # loop for (an int based on percentage of mutation with population size)
        for i in range(0, int(len(self.solutions) * MUTATION_RATE)):
            solution = random.choice(self.solutions)
            solution.mutate()

    def find_best_solution(self):
        for solution in self.solutions:
            if solution.total_distance < self.best_solution.total_distance:
                self.best_solution = solution


def ga_solve(file=None, gui=True, maxtime=MAX_TIME_ELAPSED):
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
    stagnation = 0

    while(elapsed_time < maxtime and elapsed_time >= 0 and stagnation < STAGNATION_TOLERANCE):
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
	ga_solve("data\pb005.txt", True, 5)