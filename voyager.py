# -*- coding: utf-8 -*-
from solution import Solution
import random
import functools
from copy import deepcopy
from city import City

POPULATION_SIZE = 100
MUTATION_RATE = 0.4

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
            #Choose parents and form couples
            couple = random.sample(self.solutions, 2)

            #Choose segment points
            segment_points = (random.sample(range(len(self.problem)+1), 2))
            segment_points.sort()

            #Create child based on 1st parent
            child = deepcopy(couple[0])

            #Replace inner segments cities
            inner_range = range(segment_points[0], segment_points[1])
            for i in inner_range:
                child[i] = couple[1][i]                     #Place 2nd parent value

            outter_range = (i for j in (range(segment_points[0]), range(segment_points[1], len(child.path_cities))) for i in j)
            for x in outter_range:
                if child[x] in child[segment_points[0]:segment_points[1]]:  #check if outter range contains doublons in inner range
                    child[x] = next(y for y in couple[0].path_cities if y not in child)     #Replace with missing

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