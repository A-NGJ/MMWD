import numpy as np

from abc import ABCMeta, abstractmethod
from six import add_metaclass

@add_metaclass(ABCMeta)
class ObjectiveFunction(object):

    def __init__(self, name, dim, minf, maxf):
        self.name = name
        self.dim = dim
        self.minf = minf
        self.maxf = maxf

    def sample(self):
        return np.random.uniform(low=self.minf, high=self.maxf, size=self.dim)

    def custom_sample(self):
        return np.repeat(self.minf, repeats=self.dim) \
            + np.random.uniform(low=0, high=1, size=self.dim) *\
            np.repeat(self.maxf-self.minf, repeats=self.dim)

    @abstractmethod
    def evaluate(self, x):
        pass

class Objective:
    coeB = 'jakas liczba'
    coeA = 'jakas liczba'

    def __init__(self, AVG, Tw, P, I):
        self.AVG = AVG
        self.Tw = Tw
        self.P = P
        self.I = I

    def objective_function(self):
        return (self.coeB*self.AVG + self.Tw + self.coeA*self.P)

