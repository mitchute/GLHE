from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.topology.ground_heat_exchanger_long_time_step import GroundHeatExchangerLTS
from glhe.topology.ground_heat_exchanger_short_time_step import GroundHeatExchangerSTS
from glhe.topology.borehole_types import ComponentTypes

class GroundHeatExchangerHybrid(SimulationEntryPoint):

    Type = ComponentTypes.GroundHeatExchanger

    def __init__(self, inputs, ip, op):
        self.ip = ip
        self.op = op
        self.name = 'Joey'
        self.lts_ghe = GroundHeatExchangerLTS(inputs, ip, op)
        self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)
        self.inlet_temperature = self.ip.init_temp()
        self.outlet_temperature = self.ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse):
        return SimulationResponse(SimulationResponse)

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Temperature'): self.inlet_temperature}
