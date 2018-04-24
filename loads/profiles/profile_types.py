from enum import Enum, auto


class ProfileType(Enum):
    EXTERNAL = auto()
    FIXED = auto()
    SINGLE_IMPULSE = auto()
    SINUSOID = auto()
    SYNTHETIC = auto()
