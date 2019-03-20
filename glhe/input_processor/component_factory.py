from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_temps import ExternalTemps
from glhe.profiles.flow_factory import make_flow_profile
from glhe.profiles.load_factory import make_load_profile
from glhe.topology.ground_heat_exchanger_hybrid import GroundHeatExchangerHybrid


def make_component(comp_type: str, ip: InputProcessor, op: OutputProcessor) -> object:
    if comp_type == 'flow-profile':
        inputs = ip.inputs['flow-profile']
        return make_flow_profile(inputs, ip, op)
    elif comp_type == 'load-profile':
        inputs = ip.inputs['load-profile']
        return make_load_profile(inputs, ip, op)
    elif comp_type == 'ground-heat-exchanger':
        inputs = ip.inputs['ground-heat-exchanger']
        return GroundHeatExchangerHybrid(inputs, ip, op)
    elif comp_type == 'temperature-profile':
        inputs = ip.inputs['temperature-profile']
        return ExternalTemps(inputs, ip, op)
