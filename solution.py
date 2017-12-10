# -*- coding: utf-8 -*-

import math
import random

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
            text += city.id +" "
        text += "] Distance : " + str(self.total_distance)
        return str(text)

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self, other):
        pass    #TODO greater and lesser to compare for max

    def mutate(self):
        #Select 2 different randoms
        """rand1 = random.randint(0, len(self.path_cities))
        rand2 = rand1
        while(rand2 == rand1):
            rand2 = random.randint(0, len(self.path_cities))"""

        #V2
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
            self.total_distance += math.sqrt(math.pow(self.path_cities[i+1].x - self.path_cities[i].x, 2) + math.pow(self.path_cities[i+1].y - self.path_cities[i].y, 2))
