# import numpy as np
# import pygfunction as gt
# from math import log

# from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.path import Path


# from glhe.topology.radial_numerical_borehole import RadialNumericalBH


class GroundHeatExchangerSTS(SimulationEntryPoint):
    Type = ComponentTypes.GroundHeatExchangerSTS

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.ip = ip
        self.op = op

        # props instances
        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil

        # init paths
        self.paths = []
        for path in inputs['flow-paths']:
            self.paths.append(Path(path, ip, op))

        # some stats about the bh field
        self.h = self.calc_bh_ave_length()
        self.num_bh = self.count_bhs()

        # generate the g-function data
        # self.generate_g_functions()

        # load aggregation method
        # ts = self.h ** 2 / (9 * self.soil.diffusivity)
        # la_inputs = merge_dicts(inputs['load-aggregation'], {'g-function-path': inputs['g-function-path'],
        #                                                      'time-scale': ts})
        # self.load_agg = make_agg_method(la_inputs, ip)

        # report variables
        self.heat_rate = 0
        self.heat_rate_bh = 0
        self.flow_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()

    # def generate_g_functions(self):
    #     # local variables for later use
    #     ave_pipe_outer_dia = 0
    #     ave_pipe_inner_dia = 0
    #     ave_bh_dia = 0
    #     ave_bh_resist = 0
    #     ave_pipe_conv_resist = 0
    #     ave_pipe_cp = 0
    #     ave_pipe_rho = 0
    #     ave_grout_cp = 0
    #     ave_grout_rho = 0
    #     ave_h = 0
    #
    #     # generate long time-step g-functions
    #     # these are Eskilson-type g-functions for computing the bh wall temperature rise
    #     boreholes = []
    #     for idx_path, path in enumerate(self.paths):
    #         for idx_comp, comp in enumerate(path.components):
    #             if comp.Type == ComponentTypes.BoreholeSingleUTubeGrouted:
    #                 # build out borehole field
    #                 h = comp.h
    #                 d = comp.location.z
    #                 r_b = comp.diameter / 2
    #                 x = comp.location.x
    #                 y = comp.location.y
    #                 boreholes.append(gt.boreholes.Borehole(h, d, r_b, x, y))
    #
    #                 # log average stats
    #                 temperature = 20
    #                 flow_rate = 0.2
    #                 ave_pipe_outer_dia += comp.pipe.outer_diameter
    #                 ave_pipe_inner_dia += comp.pipe.inner_diameter
    #                 ave_bh_dia += comp.diameter
    #                 ave_bh_resist += comp.calc_bh_average_resistance(temperature=temperature, flow_rate=flow_rate)
    #                 ave_pipe_conv_resist += comp.pipe.calc_conv_resist(flow_rate=flow_rate, temperature=temperature)
    #                 ave_pipe_cp += comp.pipe.specific_heat
    #                 ave_pipe_rho += comp.pipe.density
    #                 ave_grout_cp += comp.grout.specific_heat
    #                 ave_grout_rho += comp.grout.density
    #                 ave_h += comp.h
    #
    #     # generate lts g-functions using pygfunction
    #     start_time = SEC_IN_HOUR
    #     end_time = self.ip.input_dict['simulation']['runtime']
    #     ts = self.h ** 2 / (9 * self.soil.diffusivity)
    #     lntts_s = log(start_time / ts)
    #     lntts_e = log(end_time / ts)
    #     lntts_lts = np.linspace(lntts_s, lntts_e, num=30)
    #     times = np.exp(lntts_lts) * ts
    #     g_lts = gt.gfunction.uniform_temperature(boreholes, times, self.soil.diffusivity)
    #
    #     # generate sts g-functions
    #     d_sts = {'pipe-outer-diameter': ave_pipe_outer_dia,
    #              'pipe-inner-diameter': ave_pipe_inner_dia,
    #              'borehole-diameter': ave_bh_dia,
    #              'borehole-resistance': ave_bh_resist,
    #              'convection-resistance': ave_pipe_conv_resist,
    #              'fluid-specific-heat': self.fluid.get_cp(20),
    #              'fluid-density': self.fluid.get_rho(20),
    #              'pipe-specific-heat': ave_pipe_cp,
    #              'pipe-density': ave_pipe_rho,
    #              'grout-specific-heat': ave_grout_cp,
    #              'grout-density': ave_grout_rho,
    #              'soil-conductivity': self.soil.conductivity,
    #              'soil-specific-heat': self.soil.specific_heat,
    #              'soil-density': self.soil.density,
    #              'borehole-length': ave_h}
    #
    #     rn_model = RadialNumericalBH(d_sts)
    #     lntts_sts, g_sts = rn_model.calc_sts_g_functions(calculate_at_bh_wall=True)

    def calc_bh_ave_length(self):
        valid_bh_types = [ComponentTypes.BoreholeSingleUTubeGrouted]
        ave_length = 0
        count = 0
        for path in self.paths:
            for comp in path.components:
                if comp.Type in valid_bh_types:
                    ave_length += comp.h
                    count += 1

        return ave_length / count

    def count_bhs(self):
        valid_bh_types = [ComponentTypes.BoreholeSingleUTubeGrouted]
        count = 0
        for path in self.paths:
            for comp in path.components:
                if comp.Type in valid_bh_types:
                    count += 1

        return count

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        inlet_temp = inputs.temperature

        # TODO: need to distribute flow properly
        flow = inputs.flow_rate

        path_inlet_conditions = SimulationResponse(inputs.time, inputs.time_step, flow, inlet_temp)
        path_responses = []
        for path in self.paths:
            path_responses.append(path.simulate_time_step(path_inlet_conditions))

        outlet_temp = self.mix_paths(path_responses)

        # update report variables
        # TODO: generalize first-law computations everywhere
        cp = self.fluid.get_cp(inlet_temp)
        self.heat_rate = flow * cp * (inlet_temp - outlet_temp)
        self.heat_rate_bh = self.get_heat_rate_bh()
        self.inlet_temperature = inputs.temperature
        self.outlet_temperature = outlet_temp
        return SimulationResponse(inputs.time, inputs.time_step, flow, outlet_temp)

    def get_heat_rate_bh(self):
        bh_ht_rate = 0
        for path in self.paths:
            bh_ht_rate += path.get_heat_rate_bh()
        return bh_ht_rate

    def mix_paths(self, responses: list) -> float:
        sum_mdot_cp_temp = 0
        sum_mdot = 0
        sum_cp = 0
        for r in responses:
            temp = r.temperature
            m_dot = r.flow_rate
            cp = self.fluid.get_cp(temp)
            sum_mdot_cp_temp += m_dot * cp * temp
            sum_mdot += m_dot
            sum_cp += cp

        ave_cp = sum_cp / len(responses)
        return sum_mdot_cp_temp / (sum_mdot * ave_cp)

    def report_outputs(self) -> dict:
        d = {}
        for path in self.paths:
            d = merge_dicts(d, path.report_outputs())

        d_self = {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRate): self.heat_rate,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRateBH): self.heat_rate_bh,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}

        return merge_dicts(d, d_self)
