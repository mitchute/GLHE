from numpy import log10, power
from scipy.interpolate import interp1d


def log_interp1d(xx, yy, kind='linear'):
    """
    See here for details: https://stackoverflow.com/a/29359275/5965685

    :param xx: x-input range, in log-space
    :param yy: y-input range, in log-space
    :param kind: scipy interpolation type
    :return: log-interpolate function
    """

    logx = log10(xx)
    logy = log10(yy)
    lin_interp = interp1d(logx, logy, kind=kind)
    log_interp = lambda zz: power(10.0, lin_interp(log10(zz)))
    return log_interp
