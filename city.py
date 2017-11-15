#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

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