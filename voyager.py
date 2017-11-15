# -*- coding: utf-8 -*-
from solution import Solution

class Voyager:
    def __init__(self, cities):
        self.problem = cities           # Contains all cities unordered
        self.solutions = []             # Contains all solution (path that visit all cities 1 time)
        self.best_solution = None       # Contains the current best solution

        self.solutions.append(Solution(cities))   # Affect first order and reverse order to solutions
        self.solutions.append(Solution(list(reversed(cities))))

    def __str__(self):
        text = "Voyager : \n"
        for solution in self.solutions:
            text += str(solution)+"\n"
        return str(text)

    def __eq__(self, other):
        return self.id == other.id

    def apply_genetical(self):
        #TODO Select quality parents
        parent1 = self.solutions.pop()
        parent2 = self.solutions.pop()

        #TODO croisement

        #TODO mutation
        solution = list(parent1)
        solution[0], solution[1] = solution[1], solution[0] # Example switch 2 value

        self.solutions.append(solution)