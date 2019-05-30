import numpy as np
import pygfunction as gt
from math import log, pi

from glhe.aggregation.agg_factory import make_agg_method
from glhe.globals.constants import SEC_IN_DAY
from glhe.globals.functions import merge_dicts
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.path import Path
from glhe.topology.radial_numerical_borehole import RadialNumericalBH


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
        self.num_paths = len(self.paths)

        # generate the g-function data
        self.ts = self.h ** 2 / (9 * self.soil.diffusivity)
        self.lntts = None
        self.g = None
        self.lntts_b = None
        self.g_b = None

        if 'g-function-path' in inputs:
            data_g = np.genfromtxt(inputs['g-function-path'], delimiter=',')
            self.lntts = data_g[:, 0]
            self.g = data_g[:, 1]
        else:
            self.generate_g()

        # load aggregation method
        la_inputs = merge_dicts(inputs['load-aggregation'], {'lntts': self.lntts,
                                                             'g-values': self.g,
                                                             'time-scale': self.ts})
        self.load_agg = make_agg_method(la_inputs, ip)

        # other
        self.energy = 0

        # report variables
        self.heat_rate = 0
        self.heat_rate_bh = 0
        self.flow_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()
        self.bh_wall_temperature = ip.init_temp()

    def generate_g(self):
        # local variables for later use
        ave_pipe_outer_dia = 0
        ave_pipe_inner_dia = 0
        ave_bh_dia = 0
        ave_bh_resist = 0
        ave_pipe_conv_resist = 0
        ave_pipe_cp = 0
        ave_pipe_rho = 0
        ave_grout_cp = 0
        ave_grout_rho = 0
        ave_h = 0

        # generate long time-step g-functions
        # these are Eskilson-type g-functions for computing the bh wall temperature rise
        # determine "average" bh
        boreholes = []
        for idx_path, path in enumerate(self.paths):
            for idx_comp, comp in enumerate(path.components):
                if comp.Type == ComponentTypes.BoreholeSingleUTubeGrouted:
                    # build out borehole field
                    h = comp.h
                    d = comp.location.z
                    r_b = comp.diameter / 2
                    x = comp.location.x
                    y = comp.location.y
                    boreholes.append(gt.boreholes.Borehole(h, d, r_b, x, y))

                    # log average stats
                    temperature = 20
                    flow_rate = 0.2
                    ave_pipe_outer_dia += comp.pipe.outer_diameter
                    ave_pipe_inner_dia += comp.pipe.inner_diameter
                    ave_bh_dia += comp.diameter
                    ave_bh_resist += comp.calc_bh_average_resistance(temperature=temperature, flow_rate=flow_rate)
                    ave_pipe_conv_resist += comp.pipe.calc_conv_resist(flow_rate=flow_rate, temperature=temperature)
                    ave_pipe_cp += comp.pipe.specific_heat
                    ave_pipe_rho += comp.pipe.density
                    ave_grout_cp += comp.grout.specific_heat
                    ave_grout_rho += comp.grout.density
                    ave_h += comp.h

        ave_pipe_outer_dia /= self.num_bh
        ave_pipe_inner_dia /= self.num_bh
        ave_bh_dia /= self.num_bh
        ave_bh_resist /= self.num_bh
        ave_pipe_conv_resist /= self.num_bh
        ave_pipe_cp /= self.num_bh
        ave_pipe_rho /= self.num_bh
        ave_grout_cp /= self.num_bh
        ave_grout_rho /= self.num_bh
        ave_h /= self.num_bh

        # generate lts g-functions using pygfunction
        end_time = self.ip.input_dict['simulation']['runtime']
        lntts_end = log(end_time / self.ts)

        min_fls_time = SEC_IN_DAY
        lntts_start = log(min_fls_time / self.ts)

        lntts_lts = []
        g_lts = []

        if lntts_end > lntts_start:
            lntts_lts = np.arange(lntts_start, lntts_end, step=0.1)
            times = np.exp(lntts_lts) * self.ts
            g_lts = gt.gfunction.uniform_temperature(boreholes, times, self.soil.diffusivity)

        # generate sts g-functions using radial-numerical model
        d_sts = {'pipe-outer-diameter': ave_pipe_outer_dia,
                 'pipe-inner-diameter': ave_pipe_inner_dia,
                 'borehole-diameter': ave_bh_dia,
                 'borehole-resistance': ave_bh_resist,
                 'convection-resistance': ave_pipe_conv_resist,
                 'fluid-specific-heat': self.fluid.get_cp(20),
                 'fluid-density': self.fluid.get_rho(20),
                 'pipe-specific-heat': ave_pipe_cp,
                 'pipe-density': ave_pipe_rho,
                 'grout-specific-heat': ave_grout_cp,
                 'grout-density': ave_grout_rho,
                 'soil-conductivity': self.soil.conductivity,
                 'soil-specific-heat': self.soil.specific_heat,
                 'soil-density': self.soil.density,
                 'borehole-length': ave_h}

        rn_model = RadialNumericalBH(d_sts)
        lntts_sts, g_sts = rn_model.calc_sts_g_functions(final_time=min_fls_time, calculate_at_bh_wall=True)

        np.savetxt('sts.csv', (lntts_sts, g_sts), delimiter=',')
        np.savetxt('lts.csv', (lntts_lts, g_lts), delimiter=',')

        # merge the lists together
        # TODO: check if smoothing is needed between the two different g-functions
        self.lntts = np.concatenate((lntts_sts, lntts_lts))
        self.g = np.concatenate((g_sts, g_lts))

        # insert a point at a very small time so the interpolation doesn't go off the rails
        self.lntts = np.insert(self.lntts, 0, log(1 / self.ts))
        self.g = np.insert(self.g, 0, 0)
        np.savetxt('g.csv', (self.lntts, self.g), delimiter=',')

    def generate_g_b(self):

        q = 40  # W/m
        flow_rate = 0.2  # kg/s
        temperature = self.ip.init_temp()  # C

        # resistance values
        ave_bh_resist = 0
        ave_pipe_resist = 0

        for idx_path, path in enumerate(self.paths):
            for idx_comp, comp in enumerate(path.components):
                if comp.Type == ComponentTypes.BoreholeSingleUTubeGrouted:
                    ave_bh_resist += comp.calc_bh_average_resistance(temperature=temperature, flow_rate=flow_rate)
                    ave_pipe_resist += comp.pipe.calc_resist(temperature=temperature, flow_rate=flow_rate)

        ave_bh_resist /= self.num_bh
        ave_pipe_resist /= self.num_bh
        ave_grout_resist = ave_bh_resist - ave_pipe_resist

        dt = 30
        times = range(0, SEC_IN_DAY + dt, dt)
        flow_rate *= self.num_paths  # kg/s
        q_tot = q * self.num_bh * self.h  # W

        lntts_b = []
        g_b = []

        for t in times:
            cp = self.fluid.get_cp(temperature)
            temperature = temperature + q_tot / (flow_rate * cp)
            response = SimulationResponse(t, dt, flow_rate, temperature)
            temperature = self.simulate_time_step(response).temperature
            t_out = self.outlet_temperature
            t_bh = self.bh_wall_temperature
            lntts_b.append(log((t + dt) / self.ts))
            g_b.append((t_out - t_bh) / (q * ave_grout_resist))

        # TODO: check that this isn't causing errors
        # TODO: may need to add some smoothing here
        end_time = self.ip.input_dict['simulation']['runtime']
        if end_time > SEC_IN_DAY:
            lntts_b.append(log(end_time/self.ts))
            g_b.append(g_b[-1])
            self.lntts_b = lntts_b
            self.g_b = g_b

        np.savetxt('g_b.csv', (lntts_b, g_b), delimiter=',')

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

    def calc_bh_wall_temp_rise(self, time: int, time_step: int) -> float:
        self.load_agg.aggregate(time, self.energy)
        return self.load_agg.temperature_rise(time, time_step)

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        time = inputs.time
        time_step = inputs.time_step
        flow = inputs.flow_rate
        inlet_temp = inputs.temperature

        # TODO: update bh wall temp
        self.bh_wall_temperature = self.soil.get_temp(time, self.h)
        # self.bh_wall_temperature = self.soil.get_temp(time, self.h) + self.calc_bh_wall_temp_rise(time, time_step)

        # TODO: distribute flow properly

        path_inlet_conditions = SimulationResponse(inputs.time, inputs.time_step, flow, inlet_temp,
                                                   self.bh_wall_temperature)
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

        # normalized borehole wall heat transfer rate (W/m)
        q = self.heat_rate_bh / (self.h * self.num_bh)

        # energy (J/m)
        self.energy = q * time_step

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
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature,
                  '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.BHWallTemp): self.bh_wall_temperature}

        return merge_dicts(d, d_self)
