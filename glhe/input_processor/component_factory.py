from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_temps import ExternalTemps
from glhe.profiles.flow_factory import make_flow_profile
from glhe.profiles.load_factory import make_load_profile
from glhe.topology.ground_heat_exchanger import GroundHeatExchanger


def make_component(comp: dict, ip: InputProcessor, op: OutputProcessor) -> object:

    comp_type = comp['comp-type']
    comp_name = comp['name']

    inputs = ip.get_input_object(comp_type, comp_name)

    if comp_type == 'flow-profile':
        return make_flow_profile(inputs, ip, op)
    elif comp_type == 'load-profile':
        return make_load_profile(inputs, ip, op)
    elif comp_type == 'ground-heat-exchanger':
        return GroundHeatExchanger(inputs, ip, op)
    elif comp_type == 'temperature-profile':
        return ExternalTemps(inputs, ip, op)

