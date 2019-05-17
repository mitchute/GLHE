from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.properties.base_properties import PropertiesBase


class SwedishHP(PropertiesBase, SimulationEntryPoint):
    """
    Gehlin, Signhild E.A., Spitler, Jeffrey D. 2014. Design of residential ground source heat pump
    systems for heating dominated climates - trade-offs between ground heat exchanger design and
    supplementary electric resistance heating. ASHRAE Winter Conference. January 18-22. New York, NY.
    """

    Type = ComponentTypes.SwedishHP

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)

        # input/output processor
        self.ip = ip
        self.op = op

        # local fluids reference
        self.fluid = self.ip.props_mgr.fluid

        # report variables
        self.flow_rate = None
        self.outlet_temperature = None

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        return inputs

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
