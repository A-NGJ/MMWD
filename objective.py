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

    MINF = 0
    MAXF = 60
    MAXL = 9
    TS_LAB = 11.5 #h
    TD = 96 #h
    SALARY = 25 #PLN/h
    PARTY_COST = -12.5 #PLN/h
    MIN_INCOME = 500 #PLM

    def __init__(self, dim):
        super().__init__(
            'TermGraduaterObjectiveFunction',
            dim,
            TermGraduaterObjectiveFunction.MINF,
            TermGraduaterObjectiveFunction.MAXF,
            TermGraduaterObjectiveFunction.MAXL)

        self.missed_lec = 0

    def free_time(self, x: np.array):
        '''
        Returns:
            float: remaining free time
        '''
        return TermGraduaterObjectiveFunction.TD\
            -(x[1]+TermGraduaterObjectiveFunction.TS_LAB)\
            -x[0]-x[2]-x[3]

    def _satisfaction_coeff(self, x: np.array, alpha=0.008):
        '''
        Returns:
            float: satisfaction coefficient
        '''
        return (self._free_time(x) + 3*x[3])*alpha

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
        return TermGraduaterObjectiveFunction.MINF \
            + self._missed_lec_penalty(x)\
            + self._study_reward(x)


    def _max_salary(self, x: np.array):
        """
        Returns:
            float: maximum possible sary
        """
        return self._free_time(x)*TermGraduaterObjectiveFunction.SALARY

    @abstractmethod
    def evaluate(self, x):
        '''Not implemented'''


class MaximumAverageObjective(TermGraduaterObjectiveFunction):
    '''Maximum average objective function'''

    def __init__(self, dim, *, avg_coeff, salary_coeff):
        super().__init__(dim)
        self.name = 'MaximumAverageObjective'
        self.avg_coeff = avg_coeff
        self.salary_coeff = salary_coeff

    def evaluate(self, x):
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

        return self.avg_coeff*self._avg(x)+self.free_time(x)+self.salary_coeff*x[2]*MaximumAverageObjective.SALARY

    # coeB = 'jakas liczba'
    # coeA = 'jakas liczba'

    # def __init__(self, AVG, Tw, P, I):
    #     self.AVG = AVG
    #     self.Tw = Tw
    #     self.P = P
    #     self.I = I

    # def objective_function(self):
    #     return (self.coeB*self.AVG + self.Tw + self.coeA*self.P)
