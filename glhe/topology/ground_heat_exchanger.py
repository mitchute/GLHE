from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.ground_heat_exchanger_long_time_step import GroundHeatExchangerLTS
from glhe.topology.ground_heat_exchanger_short_time_step import GroundHeatExchangerSTS


class GroundHeatExchanger(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchanger

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # init TRCM model
        self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)
        ave_depth = self.sts_ghe.calc_ave_depth()
        num_bh = self.sts_ghe.count_bhs()
        lts_inputs = merge_dicts(inputs, {'depth': ave_depth, 'number-boreholes': num_bh})

        # init g-function model
        self.lts_ghe = GroundHeatExchangerLTS(lts_inputs, ip, op)

        # report variables
        self.heat_rate = 0
        self.inlet_temperature = self.ip.init_temp()
        self.outlet_temperature = self.ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse):
        response = self.lts_ghe.simulate_time_step(inputs)

        # update report variables
        self.inlet_temperature = inputs.temperature
        self.outlet_temperature = response.temperature
        m_dot = inputs.flow_rate
        cp = self.ip.props_mgr.fluid.get_cp(inputs.temperature)
        self.heat_rate = m_dot * cp * (self.inlet_temperature - self.outlet_temperature)
        return response

    def report_outputs(self):
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate}
