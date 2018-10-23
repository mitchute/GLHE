import fnmatch
import io
import os
import subprocess
import sys
import time

import pandas as pd

# shortcuts
join = os.path.join
abspath = os.path.abspath


def count_running():
    running = 0
    idle = 0

    f = call_showq()

    for line in f:
        if b'Running' and b'mitchute' in line:
            running += 1
        elif b'Idle' and b'mitchute' in line:
            idle += 1
        else:
            pass

    return running, idle


def call_showq():
    return io.BytesIO(subprocess.Popen(['showq'], stdout=subprocess.PIPE, shell=True).stdout.read())


def init_sim(path):
    print(path)
    subprocess.Popen(['qsub', 'run.pbs'], cwd=path)


def tail_file(path):
    return subprocess.Popen(['tail', path], stdout=subprocess.PIPE).stdout.read()


def find_all_jobs(path):
    jobs = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, 'run.pbs'):
                jobs.append(abspath(root))

    df = pd.DataFrame(data={'path': jobs,
                            'completed': [0] * len(jobs),
                            'errors': [0] * len(jobs)})

    return df


def count_completed_jobs_in_dir(path):
    completed = 0
    errors = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, 'run.pbs.*'):
                if b'Final runtime:' in tail_file(join(root, file)):
                    completed += 1
                else:
                    errors += 1

    return completed, errors


def count_completed_jobs(df):
    for idx, row in df.iterrows():
        completed, errors = count_completed_jobs_in_dir(row['path'])
        df.loc[idx, 'completed'] = completed
        df.loc[idx, 'errors'] = errors

    return df


def schedule_jobs(path, num_runs):
    df = find_all_jobs(path)

    max_idle = 50

    while True:

        finished = True
        df = count_completed_jobs(df)
        running, idle = count_running()

        for idx, row in df.iterrows():
            if idle < max_idle:
                if row['completed'] < int(num_runs):
                    init_sim(row['path'])
                    idle += 1
                    finished = False
                    time.sleep(5)

        if finished:
            break
        else:
            time.sleep(120)


if __name__ == "__main__":
    schedule_jobs(sys.argv[1], sys.argv[2])
