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
        df = pd.read_csv(_path, usecols=['rmse', 'run time', 'run time fraction', 'sim time', 'load'])
        df = df.loc[df["sim time"] == time]
        df = df.loc[df["load"] == load]
        return df["rmse"].tolist(), df["run time"].tolist(), df["run time fraction"].tolist()
    else:
        print('File not found: {}'.format(_path))
        return [], []


def make_plots():
    loads = ['balanced', 'imbalanced']
    times = [1, 5]

    runs = [{"name": 'Static',
             "path": '../static/runs/static_stats.csv',
             "marker": '.',
             "size": 14},
            {"name": 'Dynamic',
             "path": '../dynamic/runs/dynamic_stats.csv',
             "marker": '^',
             "size": 14},
            {"name": 'Hierarchical',
             "path": '../Hierarchical-Liu/runs/Hierarchical_stats.csv',
             "marker": 's',
             "size": 20},
            {"name": 'MLAA',
             "path": '../MLAA-Bernier/runs/MLAA_stats.csv',
             "marker": 'p',
             "size": 20},
            {"name": 'Monthly',
             "path": '../Yavuzturk/runs/Yavuzturk_stats.csv',
             "marker": 'P',
             "size": 20}
            ]

    for load in loads:
        for time in times:
            fig_1 = plt.figure()
            ax_1 = fig_1.add_subplot(1, 1, 1)

            fig_2 = plt.figure()
            ax_2 = fig_2.add_subplot(1, 1, 1)

            count = 0

            for idx, val in enumerate(runs):
                x, y_1, y_2 = extract_case_data(val["path"], load, time)

                if x and y_1 and y_2:
                    print('Processing: {}, {}_{}'.format(val["name"], load, time))
                    ax_1.scatter(x, y_1, label=val["name"], s=val["size"], marker=val["marker"])
                    ax_2.scatter(x, y_2, label=val["name"], s=val["size"], marker=val["marker"])
                    count += 1
                else:
                    print('Not found: {}, {}_{}'.format(val["name"], load, time))

            if count > 0:
                ax_1.set(xlabel=r'MFT RMSE from Non-aggregated Simulation [$^\circ$C]',
                         ylabel='Simulation Time [s]')
                ax_1.legend(loc='best')
                ax_1.grid()
                fig_1.tight_layout()
                fig_1.savefig('{}_{}.png'.format(load, time), bbox_inches='tight')

                ax_2.set(xlabel=r'MFT RMSE from Non-aggregated Simulation [$^\circ$C]',
                         ylabel='Fraction of Non-aggregated Simulation Time [-]')
                ax_2.legend(loc='best')
                ax_2.grid()
                fig_2.tight_layout()
                fig_2.savefig('{}_{}_fraction.png'.format(load, time), bbox_inches='tight')


if __name__ == "__main__":
    make_plots()
