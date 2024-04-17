from __future__ import annotations

from glhe.input_processor.input_processor import InputProcessor
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.external_flow import ExternalFlow


def make_flow_profile(inputs: dict, ip: InputProcessor) -> ConstantFlow | ExternalFlow:
    load_profile_type = inputs['flow-profile-type']
    if load_profile_type == 'constant':
        return ConstantFlow(inputs, ip)
    elif load_profile_type == 'external':
        return ExternalFlow(inputs, ip)
    else:
        raise ValueError(f"Flow profile '{load_profile_type}' is not valid.")
