import numpy as np
from food import Food

class Graduater:

    def __init__(self):
        self.T_n = Food(60, 0)
        self.T_s = Food(9, 0)
        self.T_w = Food(60, 0)
        self.P = Food(60, 0)
        self.I