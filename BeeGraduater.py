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
        if pos[2]*self.obj_function.salary < self.obj_function.min_income:
            pos[2] = self.obj_function.min_income/self.obj_function.salary
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

    def force_reset_bee(self):
        '''Resets bee regardless of its state'''
        self.__reset_bee()

    def __reset_bee(self):
        self.pos = self.obj_function.custom_sample()
        self.fitness = self.obj_function.evaluate(self.pos)
        self.trial = BaseGraduaterBee.TRIAL_INITIAL_DEFAULT_VALUE
        self.prob = BaseGraduaterBee.TRIAL_INITIAL_DEFAULT_VALUE


class EmployeeGraduaterBee(BaseGraduaterBee):
    '''Employee bee model, searches for food in the vicinity of current food source'''

    def explore(self, max_trials):
        '''Explores surroundings of current position in search of food'''
        if self.trial <= max_trials:
            component = np.random.choice(self.pos)
            phi = np.random.uniform(low=-1, high=1, size=len(self.pos))
            n_pos = self.pos + (self.pos - component) * phi
            n_pos = self.evaluate_boundaries(n_pos)
            n_fitness = self.obj_function.evaluate(n_pos)
            self.update_bee(n_pos, n_fitness)

    def get_fitness(self):
        return self.fitness*1000
    
    def compute_prob(self, max_fitness):
        self.prob = self.get_fitness() / max_fitness


class OnlookerGradueterBee(BaseGraduaterBee):
    '''Onlooker bee model, looks through the best employees and tries to improve that food source'''

    def onlook(self, best_food_sources, max_trials):
        '''Look for better source in the vicinity of current best'''
        candidate = np.random.choice(best_food_sources)
        self.__exploit(candidate.pos, candidate.fitness, max_trials)

    def __exploit(self, candidate, fitness, max_trials):
        if self.trial <= max_trials:
            component = np.random.choice(candidate)
            phi = np.random.uniform(low=-1, high=-1, size=len(candidate))
            n_pos = candidate + (candidate - component) * phi
            n_pos = self.evaluate_boundaries(n_pos)
            n_fitness = self.obj_function.evaluate(n_pos)

            if n_fitness >= fitness:
                self.pos = n_pos
                self.fitness = n_fitness
                self.trial = 0
            else:
                self.trial += 1
