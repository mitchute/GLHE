import os

import matplotlib.pyplot as plt
import pandas as pd

# shortcuts
cwd = os.getcwd()
norm = os.path.normpath
join = os.path.join


def extract_case_data(path, load, time):
    path = norm(join(cwd, path))
    df = pd.read_csv(path, usecols=['rmse', 'run time', 'sim time', 'load'])
    df = df.loc[df["sim time"] == time]
    df = df.loc[df["load"] == load]
    return df["rmse"].tolist(), df["run time"].tolist()


def make_plots():
    loads = ['balanced', 'imbalanced']
    times = [1, 5]

    runs = {1: {"name": 'Static',
                "path": '../static/runs/static_stats.csv'}}

    for load in loads:
        for time in times:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            count = 0

            for key, val in sorted(runs.items()):
                x, y = extract_case_data(val["path"], load, time)

                if x or y:
                    ax.scatter(x, y, label=val["name"])
                    count += 1

            if count > 0:
                plt.savefig('{}_{}.png'.format(load, time), bbox_inches='tight')


if __name__ == "__main__":
    make_plots()
