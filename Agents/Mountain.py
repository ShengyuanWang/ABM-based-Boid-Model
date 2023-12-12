# import packages required
import numpy as np
import random
class Mountain:

    def __init__(self, xstr=0, ystr=0, xlim=1000, ylim=1000):
        self.x = random.random()*xlim+xstr# x-position
        self.y = random.random()*ylim+ystr# y-position
