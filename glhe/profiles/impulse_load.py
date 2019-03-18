from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse


class ImpulseLoad(SimulationEntryPoint):

    def __init__(self, inputs, ip, op):

        self.load = inputs['value']
        self.start_time = inputs['start-time']
        self.end_time = inputs['end-time']
        self.ip = ip
        self.op = op

    def simulate_time_step(self, sim_time, time_step, mass_flow_rate, inlet_temp):
        if self.start_time <= sim_time < self.end_time:
            specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
            outlet_temp = self.load / (mass_flow_rate * specific_heat) + inlet_temp
            return SimulationResponse(sim_time, time_step, mass_flow_rate, outlet_temp)
        else:
            return SimulationResponse(sim_time, time_step, mass_flow_rate, inlet_temp)
