import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pprint

from ArtificialBeeColony import ABC
from Objective import MaximumAverageObjective

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

def main(parser_args):
    params = read_data(parser_args.file)
    plt.figure(figsize=(10, 7))
    simulate(MaximumAverageObjective, params['objective_params'], **params['simulation_params'])
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Json file with initial params')
    args = parser.parse_args()
    main(args)
