import numpy as np
from math import pi

from glhe.aggregation.agg_factory import make_agg_method
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.external_base import ExternalBase
from glhe.utilities.functions import merge_dicts


class GroundHeatExchangerSimple(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchangerSimple

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # props instances
        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil

        # generate the g-function data
        self.num_bh = inputs['number-boreholes']
        self.h = inputs['average-length']
        self.ts = self.h ** 2 / (9 * self.soil.diffusivity)

        data_g = np.genfromtxt(inputs['g-function-path'], delimiter=',')
        self.lntts_g = data_g[:, 0]
        self.g = data_g[:, 1]

        # load aggregation method for "self" loads
        la_self_inputs = merge_dicts(inputs['load-aggregation'], {'lntts': self.lntts_g,
                                                                  'g-values': self.g,
                                                                  'time-scale': self.ts})
        self.la_self = make_agg_method(la_self_inputs, ip)

        # g-function and load aggregation for "cross" loads
        if 'g-cross-function-path' in inputs:
            data_gx = np.genfromtxt(inputs['g-cross-function-path'], delimiter=',')
            self.lntts_gx = data_gx[:, 0]
            self.gx = data_gx[:, 1]

            la_cross_inputs = merge_dicts(inputs['load-aggregation'], {'lntts': self.lntts_gx,
                                                                       'g-values': self.gx,
                                                                       'time-scale': self.ts})
            self.la_cross = make_agg_method(la_cross_inputs, ip)
            self.cross_loads = ExternalBase(inputs['cross-loads-path'], 0)
            self.cross_ghe_present = True
        else:
            self.cross_ghe_present = False

        self.resist_b = inputs['resistance']

        # other
        self.energy = 0
        self.c_0 = 1 / (2 * pi * self.soil.conductivity)

        # report variables
        self.heat_rate = 0
        self.heat_rate_bh = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        time = inputs.time
        time_step = inputs.time_step
        flow_rate = inputs.flow_rate
        inlet_temp = inputs.temperature
        heat_rate = inputs.hp_src_heat_rate

        # self heat rate (W/m)
        q_self = heat_rate / (self.num_bh * self.h)

        # self energy (J/m)
        energy_self = q_self * time_step
        self.la_self.aggregate(time + time_step, energy_self)

        # excess temperature due to self loads
        excess_temp_self = self.la_self.calc_temporal_superposition(0) * self.c_0

        soil_temp = self.soil.get_temp(time, self.h)

        if self.cross_ghe_present:
            # cross heat rate (W/m)
            q_cross = self.cross_loads.get_value(time) / (self.num_bh * self.h)

            # cross energy (J/m)
            energy_cross = q_cross * time_step
            self.la_cross.aggregate(time + time_step, energy_cross)

            # excess temperature due to cross loads
            excess_temp_cross = self.la_cross.calc_temporal_superposition(0) * self.c_0

            borehole_temp = soil_temp + excess_temp_self + excess_temp_cross
        else:
            borehole_temp = soil_temp + excess_temp_self

        outlet_temp = 2 * (borehole_temp + q_self * self.resist_b) - inlet_temp

        cp = self.fluid.get_cp(inlet_temp)

        # update report variables
        self.heat_rate = heat_rate
        self.heat_rate_bh = flow_rate * cp * (inlet_temp - outlet_temp)
        self.inlet_temperature = inlet_temp
        self.outlet_temperature = outlet_temp

        return SimulationResponse(inputs.time, inputs.time_step, flow_rate, outlet_temp)

    def report_outputs(self) -> dict:
        d = {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
             '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRateBH): self.heat_rate_bh,
             '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
             '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
        return d
