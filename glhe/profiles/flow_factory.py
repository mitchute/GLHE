from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.fixed import Fixed


def make_flow_profile(inputs):
    load_profile_type = inputs['flow-profile-type']
    if load_profile_type == 'fixed':
        load_value = inputs['value']
        return Fixed(load_value)
    elif load_profile_type == 'external':
        path = inputs['path']
        return ExternalFlow(path)
    else:
        raise ValueError("Flow profile '{}' is not valid.".format(load_profile_type))
