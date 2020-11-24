'''Bees'''

from abc import ABC
from copy import deepcopy
import numpy as np



class BaseGraduaterBee(ABC):
    '''Base bee class'''

    TRIAL_INITIAL_DEFAULT_VALUE = 0
    INTIAL_DEFAULT_PROBABILITY = 0.0

    def __init__(self, obj_function):
        self.pos = obj_function.custom_sample()
        self.obj_function = obj_function
        self.minf = obj_function.minf
        self.maxf = obj_function.maxf
        self.maxl = obj_function.maxl
        self.fitness = obj_function.evaluate(self.pos)
        self.trial = BaseGraduaterBee.TRIAL_INITIAL_DEFAULT_VALUE
        self.prob = BaseGraduaterBee.INTIAL_DEFAULT_PROBABILITY

    def evaluate_boundaries(self, pos):
        '''
        Checks whether food is within boundaries,
        if not reevaluetes them
        Args:
            pos (np.array): variables vector
        '''
        if any(pos < self.minf) or any(pos > self.maxf):
            pos[pos > self.maxf] = self.maxf
            pos[pos < self.minf] = self.minf
        if pos[1] > self.maxl:
            pos[1] = self.maxl
        if maxw:= min(2*pos[2], self.obj_function.free_time(pos)) > pos[3]:
            pos[3] = maxw
        return pos

    def update_bee(self, pos, fitness):
        '''
        Updates bee fitness
        Args:
            pos (np.array)
            fitness (float): objective function value
        '''
        if fitness >= self.fitness:
            self.pos = pos
            self.fitness = fitness
            self.trial = 0
        else:
            self.trial += 1

    def reset_bee(self, max_trials):
        '''Resets bee if max trials number is exceeded'''
        if self.trial >= max_trials:
            self.__reset_bee()

    def __reset_bee(self):
        self.pos = self.obj_function.custom_sample()
        self.fitness = self.obj_function.evaluate(self.pos)
        self.trial = BaseGraduaterBee.TRIAL_INITIAL_DEFAULT_VALUE
        self.prob = BaseGraduaterBee.TRIAL_INITIAL_DEFAULT_VALUE

