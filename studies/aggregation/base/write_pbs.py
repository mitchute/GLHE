import os

# shortcuts
join = os.path.join
norm = os.path.normpath
cwd = os.getcwd()


def write_pbs(run_dir, time):
    pbs = ''

    with open(norm(join(cwd, '../base', 'run.pbs')), 'r') as f:
        for line in f:
            if 'SIM_RUNTIME' in line:
                pbs += line.replace('SIM_RUNTIME', time)
            elif 'PATH_TO_LOCAL_JSON_FILE' in line:
                pbs += line.replace('PATH_TO_LOCAL_JSON_FILE', join(run_dir, 'in.json'))
            else:
                pbs += line

    with open(join(run_dir, 'run.pbs'), 'w') as f:
        f.write(pbs)
