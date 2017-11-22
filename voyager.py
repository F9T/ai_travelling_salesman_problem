# -*- coding: utf-8 -*-
from solution import Solution


class Voyager:
    def __init__(self, cities):
        self.problem = cities  # Contains all cities unordered
        self.solutions = []  # Contains all solution (path that visit all cities 1 time)
        self.best_solution = None  # Contains the current best solution

        self.solutions.append(Solution(cities))  # Affect first order and reverse order to solutions
        self.solutions.append(Solution(list(reversed(cities))))

    def __str__(self):
        text = "Voyager : \n"
        for solution in self.solutions:
            text += str(solution) + "\n"
        return str(text)

    def __eq__(self, other):
        return self.id == other.id

    def apply_genetical(self):
        self.select_solutions()
        self.cross_over_solutions()
        self.mutate_solutions()
        self.find_best_solution()

    def select_solutions(self):
        # TODO select population by criters
        self.solutions = self.solutions

    def cross_over_solutions(self):
        # TODO croisement des enfants
        pass

    def mutate_solutions(self):
        for solution in self.solutions:
            solution.mutate()
        pass

    def find_best_solution(self):
        #TODO use max
        self.best_solution = self.solutions[0]  #Just to begin
        for solution in self.solutions:
            if solution.total_distance < self.best_solution.total_distance:
                self.best_solution
