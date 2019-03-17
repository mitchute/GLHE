from glhe.profiles.external_load import ExternalLoad
from glhe.profiles.fixed import Fixed
from glhe.profiles.impulse import Impulse
from glhe.profiles.sinusoid import Sinusoid
from glhe.profiles.synthetic import Synthetic


def make_load_profile(inputs):
    load_profile_type = inputs['load-profile-type']
    if load_profile_type == 'fixed':
        load_value = inputs['value']
        return Fixed(load_value)
    elif load_profile_type == 'single_impulse':
        load_start_time = inputs['start-time']
        load_end_time = inputs['end-time']
        load_value = inputs['load-value']
        return Impulse(load_value, load_start_time, load_end_time)
    elif load_profile_type == 'external':
        path = inputs['path']
        return ExternalLoad(path)
    elif load_profile_type == 'sinusoid':
        amplitude = inputs['amplitude']
        offset = inputs['offset']
        period = inputs['period']
        return Sinusoid(amplitude, offset, period)
    elif load_profile_type == 'synthetic':
        type = inputs['type']
        amplitude = inputs['amplitude']
        return Synthetic(type, amplitude)
    else:
        raise ValueError("Load profile '{}' is not valid.".format(load_profile_type))
