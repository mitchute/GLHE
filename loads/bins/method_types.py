from enum import Enum, auto


class MethodType(Enum):
    DYNAMIC = auto()
    STATIC = auto()
    NOAGG = auto()
