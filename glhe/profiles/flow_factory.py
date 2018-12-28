from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.fixed import Fixed


def make_flow_profile(inputs):
    load_profile_type = inputs['type']
    if load_profile_type == 'fixed':
        load_value = inputs['fixed']['value']
        return Fixed(load_value)
    elif load_profile_type == 'external':
        path = inputs['external']['path']
        return ExternalFlow(path)
    else:
        raise ValueError("'{}' flow profile type is not supported".format(load_profile_type))
