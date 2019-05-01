from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.properties.base_properties import PropertiesBase


class SwedishHP(PropertiesBase, SimulationEntryPoint):
    Type = ComponentTypes.SwedishHP

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)

        # input/output processor
        self.ip = ip
        self.op = op

        # local fluids reference
        self.fluid = self.ip.props_mgr.fluid

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        return inputs

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
