from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.ground_heat_exchanger_component_factory import make_ghe_component


class Path(SimulationEntryPoint):
    Type = ComponentTypes.Path

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # valid components which can exist on the path
        valid_comp_types = ['borehole', 'pipe']

        # init all components on the path
        self.components = []
        for comp in inputs['components']:
            comp_type = comp['comp-type']
            if comp_type in valid_comp_types:
                self.components.append(make_ghe_component(comp, ip, op))
            else:
                raise KeyError("Component type: '{}' is not supported by the {} object.".format(comp_type, self.Type))

        # report variables
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()
        self.flow_rate = 0

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:

        self.inlet_temperature = inputs.temperature
        response = SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, inputs.temperature)

        for comp in self.components:
            response = comp.simulate_time_step(response)

        return response

    def report_outputs(self) -> dict:
        d = {}
        for comp in self.components:
            d = merge_dicts(d, comp.report_outputs())

        d_self = {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}

        return merge_dicts(d, d_self)
