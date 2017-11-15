# -*- coding: utf-8 -*-

import math

class Solution:
    def __init__(self, path_cities):
        self.path_cities = path_cities

        # Calculate distance
        distance = 0
        for i in range(len(path_cities) - 1):   #-1 => Cause we use i+1
            distance += math.sqrt(math.pow(path_cities[i+1].x - path_cities[i].x, 2) + math.pow(path_cities[i+1].y - path_cities[i].y, 2))  #sqrt((x2-x1)^2+(y2-y1)^2)

        self.total_distance = distance

    def __str__(self):
        text = "Cities : ["
        for city in self.path_cities:
            text += city.id +" "
        text += "] Distance : " + str(self.total_distance)
        return str(text)

    def __eq__(self, other):
        return self.id == other.id
