from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.flow_factory import make_flow_profile
from glhe.profiles.load_factory import make_load_profile
from glhe.profiles.temps_factory import make_temp_profile
from glhe.topology.ground_heat_exchanger import GroundHeatExchanger
from glhe.topology.swedish_heat_pump import SwedishHP
from glhe.topology.pipe import Pipe


def make_plant_loop_component(comp: dict, ip: InputProcessor, op: OutputProcessor) -> SimulationEntryPoint:
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
        return make_temp_profile(inputs, ip, op)
    elif comp_type == 'swedish-heat-pump':
        return SwedishHP(inputs, ip, op)
    else:
        raise KeyError("Component: '{}', Name: '{}' is not valid.".format(comp_type, comp_name))
