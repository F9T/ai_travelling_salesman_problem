# -*- coding: utf-8 -*-
from solution import Solution
import random

class Voyager:
    def __init__(self, cities):
        self.problem = cities  # Contains all cities unordered
        self.solutions = []  # Contains all solution (path that visit all cities 1 time)
        self.best_solution = None  # Contains the current best solution

        #Populate
        self.solutions.append(Solution(cities))  # Affect first order and reverse order to solutions
        self.solutions.append(Solution(list(reversed(cities))))
        for i in range(98):
            self.solutions.append(Solution(sorted(cities, key=lambda k: random.random())))

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
        self.find_best_solution()

    def select_solutions(self):
        #Calculate median problem distance TODO
        median = 800

        #Select parents
        selecteds = [solution for solution in self.solutions if solution.total_distance < median]

        #Select other random to complete half of the population
        while(len(selecteds) < len(self.solutions)/2):
            selecteds.append(self.solutions[random.randint(0, len(self.solutions))])

        self.solutions = selecteds

    def cross_over_solutions(self):
        while len(self.solutions) < 100:
            #Choose parents and form couples
            couple = random.sample(self.solutions, 2)

            #Choose segment points TODO order points
            segment_points = (random.sample(range(len(self.problem)+1), 2))
            print(segment_points)

            #Create child TODO check double city
            child = couple[0]
            for i in range(len(self.problem)):
                if i >= segment_points[0] and i > segment_points[1]:
                    child[i] = couple[1][i]
            self.solutions.append(child)

        """
        |---|
        0 1 2 3 4 5
        |A|B|C|D|E|
        |B|E|C|D|A|
        """

    def mutate_solutions(self):
        for solution in self.solutions:
            solution.mutate()
        pass

    def find_best_solution(self):
        #TODO use max
        self.best_solution = self.solutions[0]  #Just to begin
        for solution in self.solutions:
            if solution.total_distance < self.best_solution.total_distance:
                self.best_solution = solution
