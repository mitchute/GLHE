import numpy as np

durations = np.array([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60])

print('1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60')

for n_60 in range(int(60 / 1) + 1):
    for n_30 in range(int(60 / 2) + 1):
        for n_20 in range(int(60 / 3) + 1):
            for n_15 in range(int(60 / 4) + 1):
                for n_12 in range(int(60 / 5) + 1):
                    for n_10 in range(int(60 / 6) + 1):
                        for n_6 in range(int(60 / 10) + 1):
                            for n_5 in range(int(60 / 12) + 1):
                                for n_4 in range(int(60 / 15) + 1):
                                    for n_3 in range(int(60 / 20) + 1):
                                        for n_2 in range(int(60 / 30) + 1):
                                            for n_1 in range(int(60 / 60) + 1):
                                                numbers = np.array([n_60,
                                                                    n_30,
                                                                    n_20,
                                                                    n_15,
                                                                    n_12,
                                                                    n_10,
                                                                    n_6,
                                                                    n_5,
                                                                    n_4,
                                                                    n_3,
                                                                    n_2,
                                                                    n_1])

                                                ret = np.dot(durations, numbers)
                                                if ret == 60:
                                                    print('{}, {}, {}, {}, {}, {}, '
                                                          '{}, {}, {}, {}, {}, {}'.format(
                                                            n_60, n_30, n_20, n_15, n_12,
                                                            n_10, n_6, n_5, n_4, n_3, n_2, n_1))
