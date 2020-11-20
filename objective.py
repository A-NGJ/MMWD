import numpy as np



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
