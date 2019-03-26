from glhe.ground_temps.constant import Constant
from glhe.ground_temps.single_harmonic import SingleHarmonic
from glhe.ground_temps.two_harmonic import TwoHarmonic


def make_ground_temp_model(inputs):
    """
    Factory method to make ground temperature model objects

    :param inputs: json blob from input file
    :return: ground temperature model object
    """

    gtm_type = inputs["ground-temperature-model-type"]
    if gtm_type == "constant":
        return Constant(inputs)
    elif gtm_type == "single-harmonic":
        return SingleHarmonic(inputs)
    elif gtm_type == "two-harmonic":
        return TwoHarmonic(inputs)
    else:
        raise ValueError("Ground temperature model '{}' is not valid.".format(gtm_type))
