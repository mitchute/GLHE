from glhe.simulation import SimulationEntryPoint, SimulationResponse
from glhe.topology.ground_heat_exchanger_long_time_step import GroundHeatExchangerLTS
from glhe.topology.ground_heat_exchanger_short_time_step import GroundHeatExchangerSTS
from glhe.functions import merge_dicts


class GroundHeatExchanger(SimulationEntryPoint):
    def __init__(self, all_inputs: dict, ghe_inputs: dict):
        SimulationEntryPoint.__init__(self, all_inputs)
        # init TRCM model
        self.sts_ghe = GroundHeatExchangerSTS(all_inputs, ghe_inputs)
        if 'g_b-function-path' not in ghe_inputs:
            if 'g_b-flow-rate' not in ghe_inputs:
                self.sts_ghe.generate_g_b(all_inputs, )
            else:
                self.sts_ghe.generate_g_b(all_inputs, ghe_inputs['g_b-flow-rate'])

        # init enhanced model
        d_bh_ave = self.sts_ghe.average_bh()
        lts_inputs = merge_dicts(ghe_inputs, {'length': self.sts_ghe.h,
                                          'number-boreholes': self.sts_ghe.num_bh,
                                          'average-borehole': d_bh_ave})

        self.lts_ghe = GroundHeatExchangerLTS(all_inputs, lts_inputs)

    def simulate_time_step(self, inputs: SimulationResponse):
        return self.lts_ghe.simulate_time_step(inputs)
        # return self.sts_ghe.simulate_time_step(response)
