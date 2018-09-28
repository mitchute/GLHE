import os

import matplotlib.pyplot as plt
import pandas as pd

# shortcuts
cwd = os.getcwd()
norm = os.path.normpath
join = os.path.join


def extract_case_data(path, load, time):
    _path = norm(join(cwd, path))
    if os.path.exists(_path):
        df = pd.read_csv(_path, usecols=['rmse', 'run time', 'sim time', 'load'])
        df = df.loc[df["sim time"] == time]
        df = df.loc[df["load"] == load]
        return df["rmse"].tolist(), df["run time"].tolist()
    else:
        print('File not found: {}'.format(_path))
        return [], []


def make_plots():
    loads = ['balanced', 'imbalanced']
    times = [1, 5]

    runs = [{"name": 'Static',
             "path": '../static/runs/static_stats.csv'},
            {"name": 'Dynamic',
             "path": '../dynamic/runs/dynamic_stats.csv'},
            {"name": 'Hierarchical',
             "path": '../Hierarchical-Liu/runs/Hierarchical_stats.csv'},
            {"name": 'MLAA',
             "path": '../MLAA-Bernier/runs/MLAA_stats.csv'},
            {"name": 'Monthly',
             "path": '../Yavuzturk/runs/Yavuzturk_stats.csv'}
            ]

    for load in loads:
        for time in times:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            count = 0

            for idx, val in enumerate(runs):
                x, y = extract_case_data(val["path"], load, time)

                if x and y:
                    print('Processing: {}, {}_{}'.format(val["name"], load, time))
                    ax.scatter(x, y, label=val["name"], s=2)
                    count += 1
                else:
                    print('Not found: {}, {}_{}'.format(val["name"], load, time))

            if count > 0:
                plt.legend()
                plt.grid()
                plt.xlabel(r'RMSE [$^\circ$C]')
                plt.ylabel('Simulation Time [s]')
                plt.savefig('{}_{}.png'.format(load, time), bbox_inches='tight')


if __name__ == "__main__":
    make_plots()
