from typing import Union

from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_temp import ConstantTemp
from glhe.profiles.external_temps import ExternalTemps


def make_temp_profile(inputs: dict, ip: InputProcessor, op: OutputProcessor) -> Union[ExternalTemps, ConstantTemp]:
    temp_profile_type = inputs['temperature-profile-type']
    if temp_profile_type == 'constant':
        return ConstantTemp(inputs, ip, op)
    elif temp_profile_type == 'external':
        return ExternalTemps(inputs, ip, op)
    else:
        raise ValueError("Temperature profile '{}' is not valid.".format(temp_profile_type))
