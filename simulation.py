from ArtificialBeeColony import ABC
from Objective import MaximumAverageObjective

import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from collections import namedtuple

def read_data(data_file):
    Coeff = namedtuple('Coeff', ['avg', 'salary'])
    try:
        data = pd.read_csv(data_file, header=None)
        print(data)
        values = data.iloc[:, :].values
        print(values)
        return Coeff(values[0][0], values[0][1])
    except EnvironmentError as err:
        print(err)

def simulate(obj_function, parameters, colony_size=30, n_iter=5000, max_trials=100, simulations=30):
    values = np.zeros(n_iter)
    for _ in range(simulations):
        optimizer = ABC(
            obj_function(4, avg_coeff=parameters.avg, salary_coeff=parameters.salary),
            colony_size=colony_size,
            n_iter=n_iter,
            max_trials=max_trials
            )
        optimizer.optimize()
        values += np.array(optimizer.optimality_tracking)
    values /= simulations

    plt.plot(np.linspace(0, n_iter-1, num=n_iter), values, lw=0.5, label='overall', color='b')
    plt.legend(loc='upper right')

def main(parser_args):
    params = read_data(parser_args.file)
    plt.figure(figsize=(10, 7))
    simulate(MaximumAverageObjective, params, simulations=1, n_iter=100)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File with csv data')
    args = parser.parse_args()
    main(args)
