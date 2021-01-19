import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import os
import pprint

from itertools import product

from ArtificialBeeColony import ABC
from objective import MaximumAverageObjective

class Simulator:

    max_fitness = 0
    max_params = None
    max_x = None

    def __init__(self, parser_args):
        self.parser_args = parser_args
        self.file_parameters = None
        self.return_dict = None

    def _read_data(self):
        try:
            with open(self.parser_args.file, "r") as df:
                data = json.load(df)
                pprint.pprint(data)
                return data
        except EnvironmentError as err:
            print(err)

    @staticmethod
    def _simulate(obj_function, obj_function_params, *, colony_size=30, n_iter=5000, max_trials=100, simulations=30):
        values = np.zeros(n_iter)
        for _ in range(simulations):
            optimizer = ABC(
                obj_function(4, **obj_function_params),
                colony_size=colony_size,
                n_iter=n_iter,
                max_trials=max_trials
                )
            optimizer.optimize()
            values += np.array(optimizer.optimality_tracking)
        values /= simulations

        plt.plot(np.linspace(0, n_iter-1, num=n_iter, dtype=int), values, lw=0.5, label='overall', color='b')
        plt.legend(loc='upper right')

    @staticmethod
    def _iter(tune_parameters):
        for p in tune_parameters:
            items = sorted(p.items())
            keys, values = zip(*items)
            for v in product(*values):
                params = dict(zip(keys, v))
                yield params

    def _tune_process(self, parameters_set):
        objective_parameters = self.file_parameters["objective_params"]
        objective_parameters.update(parameters_set)
        # print("RUNNING TUNING WITH PARAMETERS:"
        #     f"{objective_parameters}")
        optimizer = ABC(
            MaximumAverageObjective(4, **objective_parameters),
            colony_size=self.file_parameters['simulation_params']['colony_size'],
            n_iter=self.file_parameters['simulation_params']['n_iter'],
            max_trials=self.file_parameters['simulation_params']['max_trials'],
            suppress_output=True)
        fitness, x = optimizer.optimize()
        # print(f"OUTPUT FITNESS: {fitness}")
        if fitness > self.max_fitness:
            self.max_params = parameters_set
            self.max_fitness = fitness
            self.max_x = x

            print(f"{self.max_params} {self.max_fitness} {self.max_x}")
            self.return_dict["max_params"] = self.max_params
            self.return_dict["max_fitness"] = self.max_fitness
            self.return_dict["max_x"] = self.max_x

    def tune(self, tune_parameters):
        self.file_parameters = self._read_data()
        print(f"FILE PARAMETERS: {self.file_parameters}")

        max_cpus = os.cpu_count()
        if args.cpu == -1:
            processes = max_cpus
        elif args.cpu > max_cpus:
            print(f"Number of cores exceeded available cpus, using maximum {max_cpus}")
            processes = max_cpus
        else:
            processes = args.cpu

        manager = multiprocessing.Manager()
        self.return_dict = manager.dict()
        with multiprocessing.Pool(processes=processes) as pool:
            pool.map(self._tune_process, self._iter(tune_parameters))

        return self.return_dict["max_params"], self.return_dict["max_fitness"], self.return_dict["max_x"]


    def run(self):
        params = self._read_data()
        plt.figure(figsize=(10, 7))
        self._simulate(MaximumAverageObjective, params['objective_params'], **params['simulation_params'])
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument('file', help='Json file with initial params')
    tune_parser = subparsers.add_parser("tune")
    tune_parser.add_argument('file', help='Json file with initial params')
    tune_parser.add_argument('--cpu', '-c', default=1, type=int, help="Numver of cpu's used, if -1 passed all available are used")
    args = parser.parse_args()

    simulator = Simulator(args)

    if args.command == "run":
        simulator.run()
    elif args.command == "tune":

        parameters = [
            {"avg_coeff": np.arange(10, 101, step=10),
             "salary_coeff": [0.05, 0.5, 0.75, 1],
             "free_time_coeff": np.arange(1, 11)}
        ]

        best_params, best_fitness, best_position = simulator.tune(parameters)
        print(f"BEST_PARAMS: {best_params} FOR FITNESS {best_fitness} WITH POSITION {best_position}")
