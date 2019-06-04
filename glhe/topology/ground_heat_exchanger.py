import numpy as np

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

        try:
            self.sim_mode = inputs['simulation-mode']
        except KeyError:
            raise KeyError("'simulation-mode' key not found")  # pragma: no cover

        if self.sim_mode == 'enhanced':
            # init TRCM model
            self.sts_ghe = GroundHeatExchangerSTS(inputs, ip, op)

            if 'g_b-function-path' in inputs:
                data_g_b = np.genfromtxt(inputs['g_b-function-path'], delimiter=',')
                self.sts_ghe.lntts_b = data_g_b[:, 0]
                self.sts_ghe.g_b = data_g_b[:, 1]
            else:
                self.sts_ghe.generate_g_b()

            # init enhanced model
            d_bh_ave = self.sts_ghe.average_bh()
            lts_inputs = merge_dicts(inputs, {'length': self.sts_ghe.h, 'number-boreholes': self.sts_ghe.num_bh,
                                              'lntts': self.sts_ghe.lntts, 'g-values': self.sts_ghe.g,
                                              'lntts_b': self.sts_ghe.lntts_b, 'g_b-values': self.sts_ghe.g_b,
                                              'borehole-resistance': d_bh_ave['borehole-resistance'],
                                              'pipe-resistance': d_bh_ave['pipe-resistance']})

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
