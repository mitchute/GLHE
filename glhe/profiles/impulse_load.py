from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse


class ImpulseLoad(SimulationEntryPoint):

    def __init__(self, inputs, ip, op):
        self.load = inputs['value']
        self.start_time = inputs['start-time']
        self.end_time = inputs['end-time']
        self.ip = ip
        self.op = op

        # report variables
        self.outlet_temp = 0

    def simulate_time_step(self, sim_time, time_step, mass_flow_rate, inlet_temp):
        if self.start_time <= sim_time < self.end_time:
            specific_heat = self.ip.props_mgr.fluid.get_cp(inlet_temp)
            self.outlet_temp = self.load / (mass_flow_rate * specific_heat) + inlet_temp
            return SimulationResponse(sim_time, time_step, mass_flow_rate, self.outlet_temp)
        else:
            self.load = 0
            return SimulationResponse(sim_time, time_step, mass_flow_rate, inlet_temp)

    def report_outputs(self):
        return {'ImpulseLoad: temperature [C]': self.outlet_temp,
                'ImpulseLoad: load [W]': self.load}
