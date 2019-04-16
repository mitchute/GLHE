from typing import Union

from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.constant_flow import ConstantFlow
from glhe.profiles.constant_load import ConstantLoad
from glhe.profiles.external_flow import ExternalFlow
from glhe.profiles.external_load import ExternalLoad
from glhe.profiles.external_temps import ExternalTemps
from glhe.profiles.flow_factory import make_flow_profile
from glhe.profiles.load_factory import make_load_profile
from glhe.profiles.pulse_load import PulseLoad
from glhe.profiles.sinusoid_load import SinusoidLoad
from glhe.profiles.synthetic_load import SyntheticLoad
from glhe.topology.borehole_factory import make_borehole
from glhe.topology.ground_heat_exchanger import GroundHeatExchanger
from glhe.topology.pipe import Pipe


def make_component(comp: dict, ip: InputProcessor, op: OutputProcessor) -> Union[ConstantFlow, ExternalFlow,
                                                                                 ConstantLoad, PulseLoad,
                                                                                 ExternalLoad, SinusoidLoad,
                                                                                 SyntheticLoad, GroundHeatExchanger,
                                                                                 Pipe, ExternalTemps]:
    comp_type = comp['comp-type']
    comp_name = comp['name']

    inputs = ip.get_definition_object(comp_type, comp_name)

    if comp_type == 'flow-profile':
        return make_flow_profile(inputs, ip, op)
    elif comp_type == 'load-profile':
        return make_load_profile(inputs, ip, op)
    elif comp_type == 'ground-heat-exchanger':
        return GroundHeatExchanger(inputs, ip, op)
    elif comp_type == 'pipe':
        return Pipe(inputs, ip, op)
    elif comp_type == 'temperature-profile':
        return ExternalTemps(inputs, ip, op)
    elif comp_type == 'borehole':
        return make_borehole(inputs, ip, op)
    else:
        raise KeyError("Component: '{}', Name: '{}' is not valid.".format(comp_type, comp_name))
