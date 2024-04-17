from __future__ import annotations

from scp.ethyl_alcohol import EthylAlcohol
from scp.ethylene_glycol import EthyleneGlycol
from scp.methyl_alcohol import MethylAlcohol
from scp.propylene_glycol import PropyleneGlycol
from scp.water import Water


def get_fluid(inputs: dict) -> EthylAlcohol | EthyleneGlycol | MethylAlcohol | PropyleneGlycol | Water:
    fluid_type_str = inputs['fluid-type'].upper()
    if fluid_type_str == "WATER":
        concentration = 0
        return Water()
    elif fluid_type_str == "EA":
        concentration = inputs['concentration'] / 100.0
        return EthylAlcohol(concentration)
    elif fluid_type_str == "EG":
        concentration = inputs['concentration'] / 100.0
        return EthyleneGlycol(concentration)
    elif fluid_type_str == "MA":
        concentration = inputs['concentration'] / 100.0
        return MethylAlcohol(concentration)
    elif fluid_type_str == "PG":
        concentration = inputs['concentration'] / 100.0
        return PropyleneGlycol(concentration)
    else:
        raise ValueError(f"Fluid '{fluid_type_str}' fluid is not valid.")
