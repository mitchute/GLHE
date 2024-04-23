from __future__ import annotations

from glhe.input_processor.input_processor import InputProcessor
from glhe.profiles.constant_load import ConstantLoad
from glhe.profiles.external_load import ExternalLoad
from glhe.profiles.pulse_load import PulseLoad
from glhe.profiles.sinusoid_load import SinusoidLoad
from glhe.profiles.synthetic_load import SyntheticLoad


def make_load_profile(inputs: dict, ip: InputProcessor
                      ) -> ConstantLoad | PulseLoad | ExternalLoad | SinusoidLoad | SyntheticLoad:
    load_profile_type = inputs['load-profile-type']
    if load_profile_type == 'constant':
        return ConstantLoad(inputs, ip)
    elif load_profile_type == 'single-impulse':
        return PulseLoad(inputs, ip)
    elif load_profile_type == 'external':
        return ExternalLoad(inputs, ip)
    elif load_profile_type == 'sinusoid':
        return SinusoidLoad(inputs, ip)
    elif load_profile_type == 'synthetic':
        return SyntheticLoad(inputs, ip)
    else:
        raise ValueError(f"Load profile '{load_profile_type}' is not valid.")
