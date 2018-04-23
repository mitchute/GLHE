from loads.bins.dynamic import DynamicBin

if __name__ == '__main__':

    d = DynamicBin(depth=10, start_width=10, end_width=1)
    d.add_load(1)
