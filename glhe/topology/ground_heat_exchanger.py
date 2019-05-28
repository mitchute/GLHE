from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
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

        # init g-function model
        self.sts_ghe.h = self.sts_ghe.calc_bh_ave_length()
        self.sts_ghe.num_bh = self.sts_ghe.count_bhs()
        lts_inputs = merge_dicts(inputs, {'length': self.sts_ghe.h, 'number-boreholes': self.sts_ghe.num_bh,
                                          'lntts': self.sts_ghe.lntts, 'g-values': self.sts_ghe.g})
        self.lts_ghe = GroundHeatExchangerLTS(lts_inputs, ip, op)

        # report variables
        self.heat_rate = 0
        self.inlet_temperature = self.ip.init_temp()
        self.outlet_temperature = self.ip.init_temp()

        self.sim_mode = inputs['simulation-mode']

        # alias functions based on sim mode
        if self.sim_mode == 'enhanced':
            self.simulate_time_step = self.lts_ghe.simulate_time_step
            self.report_outputs = self.lts_ghe.report_outputs
        elif self.sim_mode == 'direct':
            self.simulate_time_step = self.sts_ghe.simulate_time_step
            self.report_outputs = self.sts_ghe.report_outputs
        else:
            raise KeyError("Simulation mode '{]' is not valid".format(self.sim_mode))  # pragma: no cover

    def simulate_time_step(self, inputs: SimulationResponse):
        pass  # pragma: no cover

    def report_outputs(self):
        pass  # pragma: no cover
