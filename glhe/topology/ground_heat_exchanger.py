from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.topology.ground_heat_exchanger_long_time_step import GroundHeatExchangerLTS
from glhe.topology.ground_heat_exchanger_short_time_step import GroundHeatExchangerSTS
from glhe.utilities.functions import merge_dicts


class GroundHeatExchanger(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchanger

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        try:
            self.sim_mode = inputs['simulation-mode']
        except KeyError:
            raise KeyError("'simulation-mode' key not found")  # pragma: no cover

        if self.sim_mode == 'enhanced':
            # init TRCM model
            self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)

            if 'g_b-function-path' not in inputs:
                if 'g_b-flow-rate' not in inputs:
                    self.sts_ghe.generate_g_b()
                else:
                    self.sts_ghe.generate_g_b(inputs['g_b-flow-rate'])

            # init enhanced model
            d_bh_ave = self.sts_ghe.average_bh()
            lts_inputs = merge_dicts(inputs, {'length': self.sts_ghe.h,
                                              'number-boreholes': self.sts_ghe.num_bh,
                                              'average-borehole': d_bh_ave})

            self.lts_ghe = GroundHeatExchangerLTS(lts_inputs, ip, op)

            # alias functions based on sim mode
            self.simulate_time_step = self.lts_ghe.simulate_time_step
            self.report_outputs = self.lts_ghe.report_outputs

        elif self.sim_mode == 'direct':
            # init TRCM model only
            self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)

            # alias functions based on sim mode
            self.simulate_time_step = self.sts_ghe.simulate_time_step
            self.report_outputs = self.sts_ghe.report_outputs

        else:
            raise ValueError("Simulation mode '{]' is not valid".format(self.sim_mode))  # pragma: no cover

    def simulate_time_step(self, inputs: SimulationResponse):
        pass  # pragma: no cover

    def report_outputs(self):
        pass  # pragma: no cover
