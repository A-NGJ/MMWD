'''Objective function module'''

from abc import ABC, abstractmethod
import numpy as np

class ObjectiveFunction(ABC):
    '''
    Base Objective class

    Attributes:
        name (str)
        dim (float): dimension of objective space
        minf (float): minimum value
        maxf (float): maximum value
    '''

    def __init__(self, name, dim, minf, maxf, maxl):
        self.name = name
        self.dim = dim
        self.minf = minf
        self.maxf = maxf
        self.maxl = maxl

    def sample(self):
        '''
        Returns:
            np.array: sample values.
        '''
        return np.random.uniform(low=self.minf, high=self.maxf, size=self.dim)

    def custom_sample(self):
        '''
        Returns:
            np.array: sample values calculated using custom method.
        '''
        return np.repeat(self.minf, repeats=self.dim) \
            + np.random.uniform(low=0, high=1, size=self.dim) *\
            np.repeat(self.maxf-self.minf, repeats=self.dim)

    @abstractmethod
    def evaluate(self, x):
        '''not implemented'''


class TermGraduaterObjectiveFunction(ObjectiveFunction):
    '''
    Term Graduater Objective
    Inherits from objective function
    '''

    def __init__(self, dim, *, minf, maxf, maxl, ts_lab, td, salary, party_cost, min_income):
        super().__init__(
            'TermGraduaterObjectiveFunction',
            dim, minf, maxf, maxl)

        self.td = td
        self.ts_lab = ts_lab
        self.salary = salary
        self.missed_lec = 0

    def free_time(self, x: np.array):
        '''
        Returns:
            float: remaining free time
        '''
        return self.td-(x[1]+self.ts_lab)-x[0]-x[2]-x[3]

    def _satisfaction_coeff(self, x: np.array, alpha=0.008):
        '''
        Returns:
            float: satisfaction coefficient
        '''
        return (self.free_time(x) + 3*x[3])*alpha

    def _study_reward(self, x: np.array, alpha=0.1429):
        '''
        Args:
            alpha=0.1429 (float): study reward coefficeint
        Returns:
            float: studying reward
        '''
        return alpha*(0.5*self._satisfaction_coeff(x))

    def _missed_lec_penalty(self, alpha=-0.083):
        '''
        Args:
            alpha=-0.083 (float): missed lecture penalty coefficient
        Returns:
            float: accumulated penalty for missed lectures
        '''
        return alpha*(1.5**self.missed_lec)

    def _avg(self, x: np.array):
        """
        Returns:
            float: grade average. MINF < average < MAXF
        """
        return self.minf+self._missed_lec_penalty()+self._study_reward(x)


    def _max_salary(self, x: np.array):
        """
        Returns:
            float: maximum possible sary
        """
        return self.free_time(x)*self.salary

    @abstractmethod
    def evaluate(self, x):
        '''Not implemented'''


class MaximumAverageObjective(TermGraduaterObjectiveFunction):
    '''Maximum average objective function'''

    def __init__(self, dim, *, minf=0, maxf=60, maxl=9, ts_lab=11.5, 
                 td=96, salary=25, party_cost=-12.5, min_income=500,
                 avg_coeff=1, salary_coeff=1):
        super().__init__(dim, minf=minf, maxf=maxf, maxl=maxl,
                         ts_lab=ts_lab, td=td, salary=salary,
                         party_cost=party_cost, min_income=min_income)
        self.name = 'MaximumAverageObjective'
        self.avg_coeff = avg_coeff
        self.salary_coeff = salary_coeff

    def evaluate(self, x) -> float:
        '''
        Args:
            x (np.array): position vector:
                tn - facultative learning time
                ts_lec - time spent on lectures
                tp - work time
                ti - time spent on social life
        Returns:
            Objective function value
        '''

        return self.avg_coeff*self._avg(x)+self.free_time(x)+self.salary_coeff*x[2]*self.salary

    # coeB = 'jakas liczba'
    # coeA = 'jakas liczba'

    # def __init__(self, AVG, Tw, P, I):
    #     self.AVG = AVG
    #     self.Tw = Tw
    #     self.P = P
    #     self.I = I

    # def objective_function(self):
    #     return (self.coeB*self.AVG + self.Tw + self.coeA*self.P)
