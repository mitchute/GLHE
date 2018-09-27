import os

import matplotlib.pyplot as plt

# shortcuts
cwd = os.getcwd()
norm = os.path.normpath
join = os.path.join


def extract_case_data(path, load, time):
    path = norm(join(cwd, path))

    return 0, 0


def make_plots():
    loads = ['balanced', 'imbalanced']
    times = [1, 5]

    runs = {"static": {"name": 'Static',
                       "path": '../static/runs/static_stats.csv'}}

    for load in loads:
        for time in times:
            fig = plt.figure()

            for this_run in sorted(runs):
                x, y = extract_case_data(runs[this_run]["path"], load, time)
                fig.plot(x, y, label=runs[this_run]["name"])

            plt.savefig('{}_{}.png'.format(load, time), bbox_inches='tight')


if __name__ == "__main__":
    make_plots()
