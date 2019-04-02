from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
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
        return SimulationResponse(inputs.sim_time, inputs.time_step, inputs.flow_rate, self.ip.init_temp())

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Inlet Temp.'): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, 'Outlet Temp.'): self.inlet_temperature}
