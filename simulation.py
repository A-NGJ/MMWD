import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pprint

from itertools import product

from ArtificialBeeColony import ABC
from objective import MaximumAverageObjective

def read_data(data_file):
    try:
        with open(data_file, "r") as df:
            data = json.load(df)
            pprint.pprint(data)
            return data
    except EnvironmentError as err:
        print(err)

def simulate(obj_function, obj_function_params, colony_size=30, n_iter=5000, max_trials=100, simulations=30):
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

def tune(tuned_parameters, args):
    file_parameters = read_data(args.file)
    print(f"FILE PARAMETERS: {file_parameters}")

    def _iter():
        for p in tuned_parameters:
            items = sorted(p.items())
            keys, values = zip(*items)
            for v in product(*values):
                params = dict(zip(keys, v))
                yield params

    max_fitness = 0
    for parameters_set in _iter():
        objective_parameters = file_parameters["objective_params"]
        objective_parameters.update(parameters_set)
        print("RUNNING TUNING WITH PARAMETERS:"
               f"{objective_parameters}")
        optimizer = ABC(
            MaximumAverageObjective(4, **objective_parameters),
            colony_size=file_parameters['simulation_params']['colony_size'],
            n_iter=file_parameters['simulation_params']['n_iter'],
            max_trials=file_parameters['simulation_params']['max_trials'],
            suppress_output=True)
        fitness, x = optimizer.optimize()
        print(f"OUTPUT FITNESS: {fitness}")
        if fitness > max_fitness:
            max_params = parameters_set
            max_fitness = fitness
            max_x = x

    return max_params, max_fitness, max_x

def main(parser_args):
    params = read_data(parser_args.file)
    plt.figure(figsize=(10, 7))
    simulate(MaximumAverageObjective, params['objective_params'], **params['simulation_params'])
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument('file', help='Json file with initial params')
    tune_parser = subparsers.add_parser("tune")
    tune_parser.add_argument('file', help='Json file with initial params')
    args = parser.parse_args()

    if args.command == "run":
        main(args)
    elif args.command == "tune":

        parameters = [
            {"avg_coeff": np.arange(10, 101, step=10),
             "salary_coeff": [0.05, 0.5, 0.75, 1],
             "free_time_coeff": np.arange(1, 11)}
        ]

        best_params, best_fitness, best_position = tune(parameters, args)
        print(f"BEST_PARAMS: {best_params} FOR FITNESS {best_fitness} WITH POSITION {best_position}")
