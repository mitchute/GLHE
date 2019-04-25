from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.borehole_factory import make_borehole
from glhe.topology.pipe import Pipe


def make_ghe_component(comp: dict, ip: InputProcessor, op: OutputProcessor) -> SimulationEntryPoint:
    comp_type = comp['comp-type']
    comp_name = comp['name']

    if comp_type == 'pipe':
        inputs = ip.get_definition_object(comp_type, comp_name)
        return Pipe(inputs, ip, op)
    elif comp_type == 'borehole':
        return make_borehole(comp, ip, op)
    else:
        raise KeyError("Component: '{}', Name: '{}' is not valid.".format(comp_type, comp_name))  # pragma: no cover
