import os
import subprocess
import sys

# shortcuts
join = os.path.join


def call_cd(path):
    print(os.getcwd())
    subprocess.call(['cd', path])
    print(os.getcwd())


def init_sim():
    return subprocess.call(['ls', 'run.pbs'])


def call_tail(path):
    return subprocess.Popen(['tail', path], stdout=subprocess.PIPE).stdout.read()


def find_all_jobs(path):
    return call_cd(path)

    # df = pd.DataFrame(colums)

    # for root, dirs, files in os.walk(path):


def schedule_jobs(path, num_runs):
    tail = find_all_jobs(path)
    print(tail)


if __name__ == "__main__":
    schedule_jobs(sys.argv[1], sys.argv[2])
