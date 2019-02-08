import datetime
from scipy.interpolate import interp1d
from numpy import arange

from random import random

from glhe.properties.fluid import Fluid

f = Fluid({'name': 'water', 'type': 'water'})

temps = [x for x in arange(0, 55, 0.1)]
props = [f.calc_density(x) for x in temps]

f_prop = interp1d(temps, props)


num_iter = 1000

rands = [random() * 50 for _ in range(num_iter)]

start_time = datetime.datetime.now()

for idx, val in enumerate(rands):
    f_prop(val)

time = datetime.datetime.now() - start_time

time /= num_iter

print("Calc directly: {}s".format(time))
