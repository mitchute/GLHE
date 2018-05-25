import six

if six.PY2:
    from enum34 import Enum
elif six.PY3:
    from enum import Enum


class SegmentType(Enum):
    SIMPLE = 1
