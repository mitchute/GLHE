import os

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def write_pbs(run_dir, time, num_up, kill):
    pbs = ''

    with open(norm(join(cwd, '../base', 'run.pbs')), 'r') as f:
        for line in f:

            if kill:
                if 'batch' in line:
                    line = line.replace('batch', 'killable')

            if 'SIM_RUNTIME' in line:
                line = line.replace('SIM_RUNTIME', time)

            if 'PATH_TO_LOCAL_JSON_FILE' in line:
                line = line.replace('PATH_TO_LOCAL_JSON_FILE', join(run_dir, 'in.json'))

            if 'NUM_DIRS_UP_FOR_PATH' in line:
                line = line.replace('NUM_DIRS_UP_FOR_PATH', str(num_up))

            pbs += line

    with open(join(run_dir, 'run.pbs'), 'w') as f:
        f.write(pbs)
