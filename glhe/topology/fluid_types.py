import six

if six.PY2:
    from enum34 import Enum
elif six.PY3:
    from enum import Enum


class FluidType(Enum):
    WATER = 1
    ETHYL_ALCOHOL = 2
    ETHYLENE_GLYCOL = 3
    PROPYLENE_GLYCOL = 4
