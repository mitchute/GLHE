from glhe.aggregation.agg_method_factory import make_agg_method
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor


class GroundHeatExchangerLTS(SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs['name'])
        self.ip = ip
        self.op = op
        self.load_agg = make_agg_method(inputs['load-aggregation'], ip, op)

    def simulate_time_step(self, inputs: SimulationResponse):
        return inputs

    def report_outputs(self):
        pass
