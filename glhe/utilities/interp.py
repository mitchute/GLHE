import numpy as np
from scipy.interpolate.interpolate import interp2d


class Interp2Vars(object):

    def __init__(self, xz_data_path: str, y: list):

        """
        Intended to interpolate simple data with two independent variables

        Example:
        x1, y1, z1, x2, y2, z2\n
        1,   3,  5,  1,  4,  6\n
        2,   3,  6,  2,  4,  7\n
        3,   3   7,  3,  4,  8\n

        xy_data_path will lead to a file such as:

        1,5,6\n
        2,6,7\n
        3,7,8\n

        y will be: [3, 4]

        :param xz_data_path: path to csv file with columnated data, e.g. 'x1,z1,z2,...,zn'
        :param y: list of *constant* values for the second independent variable
        """

        data = np.genfromtxt(xz_data_path, delimiter=',')
        _, nz = data.shape

        num_series = nz - 1

        # check to make sure number of columns and length of 'y' match
        if num_series != len(y):
            ValueError("Number of columns in '{}' inconsistent with 'y'".format(xz_data_path))

        x = data[:, 0]
        z = []
        for idx in range(1, num_series + 1):
            z.append(data[:, idx])

        self.interp = interp2d(x, y, z)

    def get_value(self, x, y):
        return self.interp(x, y)
