from glhe.groundTemps.constant import Constant
from glhe.groundTemps.single_harmonic import SingleHarmonic
from glhe.groundTemps.two_harmonic import TwoHarmonic


def ground_temperature_model_factory(inputs):
    """
    Factory method to make ground temperature model objects

    :param inputs: json blob from input file
    :return: ground temperature model object
    """

    gtm_type = inputs["type"]
    if gtm_type == "constant":
        return Constant(inputs["constant"]["temperature"])
    elif gtm_type == "single-harmonic":
        return SingleHarmonic(inputs["single-harmonic"]["ave-temperature"],
                              inputs["single-harmonic"]["amplitude"],
                              inputs["single-harmonic"]["phase-shift"],
                              inputs["soil-diffusivity"])
    elif gtm_type == "two-harmonic":
        return TwoHarmonic(inputs["two-harmonic"]["ave-temperature"],
                           inputs["two-harmonic"]["amplitude-1"],
                           inputs["two-harmonic"]["amplitude-2"],
                           inputs["two-harmonic"]["phase-shift-1"],
                           inputs["two-harmonic"]["phase-shift-2"],
                           inputs["soil-diffusivity"])
    else:
        raise ValueError("'{}' ground temperature type is not supported".format(gtm_type))
