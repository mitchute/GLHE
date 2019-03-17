from glhe.inputProcessor.input_processor import InputProcessor
from glhe.outputProcessor.output_processor import OutputProcessor
from glhe.profiles.flow_factory import make_flow_profile
from glhe.profiles.load_factory import make_load_profile

from glhe.topology.ground_heat_exchanger import GroundHeatExchanger


def make_component(comp_type: str, ip: InputProcessor, op: OutputProcessor) -> object:
    if comp_type == 'flow-profile':
        inputs = ip.inputs['flow-profile']
        return make_flow_profile(inputs)
    elif comp_type == 'load-profile':
        inputs = ip.inputs['load-profile']
        return make_load_profile(inputs)
    elif comp_type == 'ground-heat-exchanger':
        inputs = ip.inputs['ground-heat-exchanger']
        return GroundHeatExchanger(inputs, ip, op)
