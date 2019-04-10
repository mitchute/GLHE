from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.ground_heat_exchanger_long_time_step import GroundHeatExchangerLTS
from glhe.topology.ground_heat_exchanger_short_time_step import GroundHeatExchangerSTS


class GroundHeatExchanger(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchanger

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs['name'])
        self.ip = ip
        self.op = op
        self.lts_ghe = GroundHeatExchangerLTS(inputs, ip, op)
        self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)
        self.inlet_temperature = self.ip.init_temp()
        self.outlet_temperature = self.ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse):
        response = self.lts_ghe.simulate_time_step(inputs)

        # update report variables
        self.inlet_temperature = inputs.temperature
        self.outlet_temperature = response.temperature
        return response

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
