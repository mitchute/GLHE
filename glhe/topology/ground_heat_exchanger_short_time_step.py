import os

import numpy as np
import pygfunction as gt
from math import log, pi

from glhe.aggregation.agg_factory import make_agg_method
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.output_processor.report_types import ReportTypes
from glhe.topology.borehole_factory import make_borehole
from glhe.topology.path import Path
from glhe.topology.radial_numerical_borehole import RadialNumericalBH
from glhe.utilities.constants import SEC_IN_DAY
from glhe.utilities.functions import merge_dicts
from glhe.utilities.functions import resample_g_functions
from glhe.utilities.functions import write_arrays_to_csv

cwd = os.getcwd()


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
        self.c_0 = 1 / (2 * pi * self.soil.conductivity)

        # report variables
        self.heat_rate = 0
        self.heat_rate_bh = 0
        self.flow_rate = 0
        self.inlet_temperature = ip.init_temp()
        self.outlet_temperature = ip.init_temp()
        self.bh_wall_temperature = ip.init_temp()

    def average_bh(self):
        # local variables for later use
        ave_pipe_outer_dia = 0
        ave_pipe_inner_dia = 0
        ave_bh_dia = 0
        ave_bh_resist = 0
        ave_pipe_resist = 0
        ave_pipe_conv_resist = 0
        ave_pipe_k = 0
        ave_pipe_cp = 0
        ave_pipe_rho = 0
        ave_grout_k = 0
        ave_grout_cp = 0
        ave_grout_rho = 0
        ave_h = 0
        ave_shank_space = 0

        # determine "average" bh
        for idx_path, path in enumerate(self.paths):
            for idx_comp, comp in enumerate(path.components):
                if comp.Type == ComponentTypes.BoreholeSingleUTubeGrouted:
                    # log average stats
                    temperature = 20
                    flow_rate = 0.2
                    ave_pipe_outer_dia += comp.pipe.outer_diameter
                    ave_pipe_inner_dia += comp.pipe.inner_diameter
                    ave_bh_dia += comp.diameter
                    ave_bh_resist += comp.calc_bh_average_resistance(temperature=temperature, flow_rate=flow_rate)
                    ave_pipe_resist += comp.pipe.calc_resist(flow_rate=flow_rate, temperature=temperature)
                    ave_pipe_conv_resist += comp.pipe.calc_conv_resist(flow_rate=flow_rate, temperature=temperature)
                    ave_pipe_k += comp.pipe.conductivity
                    ave_pipe_cp += comp.pipe.specific_heat
                    ave_pipe_rho += comp.pipe.density
                    ave_grout_k += comp.grout.conductivity
                    ave_grout_cp += comp.grout.specific_heat
                    ave_grout_rho += comp.grout.density
                    ave_h += comp.h
                    ave_shank_space += comp.shank_space

        d = {'pipe-outer-diameter': ave_pipe_outer_dia / self.num_bh,
             'pipe-inner-diameter': ave_pipe_inner_dia / self.num_bh,
             'diameter': ave_bh_dia / self.num_bh,
             'borehole-resistance': ave_bh_resist / self.num_bh,
             'pipe-resistance': ave_pipe_resist / self.num_bh,
             'pipe-conv-resistance': ave_pipe_conv_resist / self.num_bh,
             'pipe-conductivity': ave_pipe_k / self.num_bh,
             'pipe-specific-heat': ave_pipe_cp / self.num_bh,
             'pipe-density': ave_pipe_rho / self.num_bh,
             'grout-conductivity': ave_grout_k / self.num_bh,
             'grout-specific-heat': ave_grout_cp / self.num_bh,
             'grout-density': ave_grout_rho / self.num_bh,
             'length': ave_h / self.num_bh,
             'shank-spacing': ave_shank_space / self.num_bh}

        return d

    def generate_g(self):
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

        # generate lts g-functions using pygfunction
        end_time = self.ip.input_dict['simulation']['runtime']
        lntts_end = log(end_time / self.ts)

        min_fls_time = SEC_IN_DAY
        lntts_start = log(min_fls_time / self.ts)

        lntts_lts = []
        g_lts = []

        if end_time > min_fls_time:
            lntts_lts = np.arange(lntts_start, lntts_end, step=0.1)
            times = np.exp(lntts_lts) * self.ts
            g_lts = gt.gfunction.uniform_temperature(boreholes, times, self.soil.diffusivity)

        # generate sts g-functions using radial-numerical model
        d_ave_bh = self.average_bh()
        d_sts = {'pipe-outer-diameter': d_ave_bh['pipe-outer-diameter'],
                 'pipe-inner-diameter': d_ave_bh['pipe-inner-diameter'],
                 'diameter': d_ave_bh['diameter'],
                 'borehole-resistance': d_ave_bh['borehole-resistance'],
                 'convection-resistance': d_ave_bh['pipe-conv-resistance'],
                 'fluid-specific-heat': self.fluid.get_cp(20),
                 'fluid-density': self.fluid.get_rho(20),
                 'pipe-conductivity': d_ave_bh['pipe-conductivity'],
                 'pipe-specific-heat': d_ave_bh['pipe-specific-heat'],
                 'pipe-density': d_ave_bh['pipe-density'],
                 'grout-conductivity': d_ave_bh['grout-conductivity'],
                 'grout-density': d_ave_bh['grout-density'],
                 'grout-specific-heat': d_ave_bh['grout-specific-heat'],
                 'soil-conductivity': self.soil.conductivity,
                 'soil-specific-heat': self.soil.specific_heat,
                 'soil-density': self.soil.density,
                 'shank-spacing': d_ave_bh['shank-spacing'],
                 'length': d_ave_bh['length']}

        rn_model = RadialNumericalBH(d_sts)
        lntts_sts, g_sts = rn_model.calc_sts_g_functions(final_time=min_fls_time, calculate_at_bh_wall=True)

        write_arrays_to_csv(os.path.join(cwd, 'sts.csv'), [lntts_sts, g_sts])
        write_arrays_to_csv(os.path.join(cwd, 'lts.csv'), [lntts_lts, g_lts])

        # merge the lists together
        # TODO: check if smoothing is needed between the two different g-functions
        self.lntts = np.concatenate((lntts_sts, lntts_lts))
        self.g = np.concatenate((g_sts, g_lts))

        # insert a point at a very small time so the interpolation doesn't go off the rails
        self.lntts = np.insert(self.lntts, 0, log(30 / self.ts))
        self.g = np.insert(self.g, 0, 0)
        write_arrays_to_csv(os.path.join(cwd, 'g.csv'), [self.lntts, self.g])

    def generate_g_b(self, flow_rate=0.5):

        q = 10  # W/m
        flow_rate = flow_rate
        flow_rate_path = flow_rate / self.num_paths  # kg/s
        temperature = self.ip.init_temp()  # C

        d_ave_bh = {'average-borehole': self.average_bh()}
        d_ave_bh['name'] = 'average-borehole'
        d_ave_bh['borehole-type'] = 'single-grouted'
        ave_bh = make_borehole(d_ave_bh, self.ip, self.op)

        dt = 30
        times = range(0, SEC_IN_DAY + dt, dt)
        q_tot = q * self.num_bh * self.h  # W
        r_b = ave_bh.calc_bh_average_resistance(temperature, flow_rate_path)

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
            g_b.append((t_out - t_bh) / (q * r_b))

        # check for convergence
        err = (g_b[-1] - g_b[-2]) / (lntts_b[-1] - lntts_b[-2])

        t = times[-1]
        end_time = self.ip.input_dict['simulation']['runtime']
        while err > 0.02:
            t += dt
            cp = self.fluid.get_cp(temperature)
            temperature = temperature + q_tot / (flow_rate * cp)
            response = SimulationResponse(t, dt, flow_rate, temperature)
            temperature = self.simulate_time_step(response).temperature
            t_out = self.outlet_temperature
            t_bh = self.bh_wall_temperature
            lntts_b.append(log((t + dt) / self.ts))
            g_b.append((t_out - t_bh) / (q * r_b))
            err = (g_b[-1] - g_b[-2]) / (lntts_b[-1] - lntts_b[-2])
            if t > end_time:
                break

        # add point at end time
        if end_time > t:
            lntts_b.append(log(end_time / self.ts))
            g_b.append(g_b[-1])

        self.lntts_b, self.g_b = resample_g_functions(lntts_b, g_b, lntts_interval=0.1)

        write_arrays_to_csv(os.path.join(cwd, 'g_b.csv'), [self.lntts_b, self.g_b])

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
        hist = self.load_agg.calc_temporal_superposition(time_step)
        return hist * self.c_0

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        time = inputs.time
        time_step = inputs.time_step
        flow = inputs.flow_rate
        inlet_temp = inputs.temperature

        # TODO: update bh wall temp
        # self.bh_wall_temperature = self.soil.get_temp(time, self.h)
        self.bh_wall_temperature = self.soil.get_temp(time, self.h) + self.calc_bh_wall_temp_rise(time, time_step)

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
