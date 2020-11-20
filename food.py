import numpy as np


class Food:

    def __init__(self, u_i, l_i):
        self.u_i: int = u_i
        self.l_i: int = l_i
        self.vect: np.array = np.arange(u_i, dtype=int)