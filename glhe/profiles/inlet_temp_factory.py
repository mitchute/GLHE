from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_inlet_temps import ExternalInletTemps


def make_inlet_temp_profile(inputs: dict, ip: InputProcessor, op: OutputProcessor):
    return ExternalInletTemps(inputs, ip, op)
