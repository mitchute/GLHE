from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.constant_flow import ConstantFlow


def make_flow_profile(inputs: dict) -> object:
    load_profile_type = inputs['flow-profile-type']
    if load_profile_type == 'constant':
        flow_value = inputs['value']
        return ConstantFlow(flow_value)
    elif load_profile_type == 'external':
        path = inputs['path']
        return ExternalFlow(path)
    else:
        raise ValueError("Flow profile '{}' is not valid.".format(load_profile_type))
