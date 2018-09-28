import os

import matplotlib.pyplot as plt
import pandas as pd

# shortcuts
cwd = os.getcwd()
norm = os.path.normpath
join = os.path.join


def extract_case_data(path, load, time):
    if os.path.exists(path):
        path = norm(join(cwd, path))
        df = pd.read_csv(path, usecols=['rmse', 'run time', 'sim time', 'load'])
        df = df.loc[df["sim time"] == time]
        df = df.loc[df["load"] == load]
        return df["rmse"].tolist(), df["run time"].tolist()
    else:
        return [], []


def make_plots():
    loads = ['balanced', 'imbalanced']
    times = [1, 5]

    runs = [{"name": 'Static',
             "path": '../static/runs/static_stats.csv'},
            {"name": 'Dynamic',
             "path": '../dynamic/runs/dynamic_stats.csv'},
            {"name": 'Hierarchical',
             "path": '../Hierarchical-Liu/runs/Hierarchical-stats.csv'},
            {"name": 'MLAA',
             "path": '../MLAA-Bernier/runs/MLAA-stats.csv'},
            {"name": 'Monthly',
             "path": '../Yavuzturk/runs/Yavuzturk-stats.csv'}
            ]

    for load in loads:
        for time in times:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            count = 0

            for idx, val in enumerate(runs):

                print('Processing: Method={}, load={}, run time={}'.format(val["name"], load, time))

                x, y = extract_case_data(val["path"], load, time)

                if x and y:
                    ax.scatter(x, y, label=val["name"], s=2)
                    count += 1

            if count > 0:

                plt.legend()
                plt.grid()
                plt.xlabel(r'RMSE [$^\circ$C]')
                plt.ylabel('Simulation Time [s]')
                plt.savefig('{}_{}.png'.format(load, time), bbox_inches='tight')


if __name__ == "__main__":
    make_plots()
