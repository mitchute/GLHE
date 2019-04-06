from enum import Enum


class AggregationTypes(Enum):
    NO_AGG = 'NO-AGG'
    STATIC = 'STATIC'
    SUB_HOUR = 'SUB-HOUR'
    DYNAMIC = 'DYNAMIC'
