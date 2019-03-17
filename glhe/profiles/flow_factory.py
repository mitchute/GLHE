from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.constant_flow import ConstantFlow
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor

def make_flow_profile(inputs: dict, ip: InputProcessor, op: OutputProcessor) -> object:
    load_profile_type = inputs['flow-profile-type']
    if load_profile_type == 'constant':
        return ConstantFlow(inputs, ip, op)
    elif load_profile_type == 'external':
        return ExternalFlow(inputs, ip, op)
    else:
        raise ValueError("Flow profile '{}' is not valid.".format(load_profile_type))
