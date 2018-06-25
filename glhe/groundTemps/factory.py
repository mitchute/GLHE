from glhe.groundTemps.constant import Constant
from glhe.groundTemps.single_harmonic import SingleHarmonic
from glhe.groundTemps.two_harmonic import TwoHarmonic


def make_ground_temperature_model(inputs):
    gtm_type = inputs["type"]
    if gtm_type == "constant":
        return Constant(inputs["temperature"])
    elif gtm_type == "single-harmonic":
        return SingleHarmonic(inputs["ave-temperature"],
                              inputs["amplitude"],
                              inputs["phase-shift"],
                              inputs["soil-diffusivity"])
    elif gtm_type == "two-harmonic":
        return TwoHarmonic(inputs["ave-temperature"],
                           inputs["amplitude-1"],
                           inputs["amplitude-2"],
                           inputs["phase-shift-1"],
                           inputs["phase-shift-2"],
                           inputs["soil-diffusivity"])
    else:
        raise ValueError("'{}' ground temperature type is not supported".format(gtm_type))
