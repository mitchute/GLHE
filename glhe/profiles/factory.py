from glhe.profiles.fixed import Fixed
from glhe.profiles.impulse import Impulse
from glhe.profiles.external import External
from glhe.profiles.sinusoid import Sinusoid
from glhe.profiles.synthetic import Synthetic


def make_load_profile(inputs):
    load_profile_type = inputs['type']
    if load_profile_type == 'fixed':
        load_value = inputs['fixed']['value']
        return Fixed(load_value)
    elif load_profile_type == 'single_impulse':
        load_start_time = inputs['single_impulse']['start-time']
        load_end_time = inputs['single_impulse']['end-time']
        load_value = inputs['single_impulse']['load-value']
        return Impulse(load_value, load_start_time, load_end_time)
    elif load_profile_type == 'external':
        path = inputs['external']['path']
        return External(path)
    elif load_profile_type == 'sinusoid':
        amplitude = inputs['sinusoid']['amplitude']
        offset = inputs['sinusoid']['offset']
        period = inputs['sinusoid']['period']
        return Sinusoid(amplitude, offset, period)
    elif load_profile_type == 'synthetic':
        type = inputs['synthetic']['type']
        amplitude = inputs['synthetic']['amplitude']
        return Synthetic(type, amplitude)
