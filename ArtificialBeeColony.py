from copy import deepcopy
import numpy as np

from BeeGraduater import EmployeeGraduaterBee, OnlookerGradueterBee

class ABC(object):

    def __init__(self, obj_function, colony_size=30, n_iter=5000, max_trials=100):
        self.colony_size = colony_size
        self.obj_function = obj_function

        self.n_iter = n_iter
        self.max_trials = max_trials

        self.optimal_solution = None
        self.prev_optimal_solution = None
        self.optimal_solution_iter = 0
        self.optimality_tracking = []

        self.employee_bees = []
        self.onlokeer_bees = []

    def __reset_algorithm(self):
        self.optimal_solution = None
        self.optimality_tracking = []

    def __update_optimality_tracking(self):
        self.optimality_tracking.append(self.optimal_solution.fitness)

    def __update_optimal_solution(self, iter_):
        n_optimal_solution = \
            max(self.onlokeer_bees + self.employee_bees,
                key=lambda bee: bee.fitness)
        if iter_ == 1:
            self.prev_optimal_solution = self.optimal_solution
        if not self.optimal_solution:
            self.optimal_solution = deepcopy(n_optimal_solution)
        else:
            if np.array_equal(self.prev_optimal_solution.pos, self.optimal_solution.pos):
                self.optimal_solution_iter += 1
            if (self.optimal_solution_iter == self.obj_function.max_iter) and \
               ((self.n_iter -  iter_) / self.n_iter) > 0.1:
                self.__reset_bees()
            elif n_optimal_solution.fitness > self.optimal_solution.fitness:
                self.optimal_solution = deepcopy(n_optimal_solution)
        self.prev_optimal_solution = deepcopy(self.optimal_solution)

    def __initialize_employees(self):
        for _ in range(self.colony_size // 2):
            self.employee_bees.append(EmployeeGraduaterBee(self.obj_function))

    def __initialize_onlookers(self):
        for _ in range(self.colony_size // 2):
            self.onlokeer_bees.append(OnlookerGradueterBee(self.obj_function))

    def __reset_bees(self):
        self.optimal_solution_iter = 0
        list(map(lambda bee: bee.force_reset_bee(), self.employee_bees + self.onlokeer_bees))
        self.optimal_solution = np.random.choice(self.employee_bees + self.onlokeer_bees)

    def __employee_bees_phase(self):
        list(map(lambda bee: bee.explore(self.max_trials), self.employee_bees))

    def __calculate_probabilities(self):
        sum_fitness = sum(map(lambda bee: bee.get_fitness(), self.employee_bees))
        list(map(lambda bee: bee.compute_prob(sum_fitness), self.employee_bees))

    def __select_best_food_sources(self):
        self.best_food_sources =\
            list(filter(lambda bee: bee.prob > np.random.uniform(low=0, high=1),
                   self.employee_bees))
        while not self.best_food_sources:
            self.best_food_sources = \
                list(filter(lambda bee: bee.prob > np.random.uniform(low=0, high=1),
                       self.employee_bees))

    def __onlooker_bees_phase(self):
        list(map(lambda bee: bee.onlook(self.best_food_sources, self.max_trials),
            self.onlokeer_bees))

    def __scout_bees_phase(self):
        list(map(lambda bee: bee.reset_bee(self.max_trials),
            self.onlokeer_bees + self.employee_bees))

    def optimize(self):
        self.__reset_algorithm()
        self.__initialize_employees()
        self.__initialize_onlookers()
        for itr in range(self.n_iter):
            self.__employee_bees_phase()
            self.__update_optimal_solution(itr)

            self.__calculate_probabilities()
            self.__select_best_food_sources()

            self.__onlooker_bees_phase()
            self.__scout_bees_phase()

            self.__update_optimal_solution(itr)
            self.__update_optimality_tracking()
            print(self.optimal_solution.pos)
            print("iter: {} = cost: {}"
                  .format(itr, "%04.03e" % self.optimal_solution.fitness))
