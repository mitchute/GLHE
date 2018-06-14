from loads.profiles.fixed import Fixed
from loads.profiles.single_impulse import SingleImpulse


def make_load_profile(inputs):
    load_profile_type = inputs['type']
    if load_profile_type == 'fixed':
        load_value = inputs['fixed']['value']
        return Fixed(load_value)
    elif load_profile_type == 'single_impulse':
        load_start_time = inputs['single_impulse']['start-time']
        load_end_time = inputs['single_impulse']['end-time']
        load_value = inputs['single_impulse']['load-value']
        return SingleImpulse(load_value, load_start_time, load_end_time)
