import datetime
import os
import sys

from scipy.optimize import minimize

from glhe.gFunction.g_function import GFunction
from glhe.globals.errors import SimulationError
from glhe.globals.functions import set_time_step
from glhe.globals.variables import gv
from glhe.inputProcessor.processor import InputProcessor
from glhe.interface.response import TimeStepSimulationResponse
from glhe.outputProcessor.processor import OutputProcessor
from glhe.profiles.factory_flow import make_flow_profile
from glhe.profiles.factory_inlet_temp import make_inlet_temp_profile
from glhe.profiles.factory_load import make_load_profile
from glhe.properties.fluid import Fluid


class RunGFunctions(object):
    def __init__(self, input_file_path):

        # get input from file
        d = InputProcessor().process_input(input_file_path)

        # output processor
        self.op = OutputProcessor()

        # set the global level time-step
        gv.time_step = set_time_step(d['simulation']['time-steps per hour'])

        # init the g-function object and resister the output variables after init
        self.g = GFunction(d)

        self.run_time = d['simulation']['runtime']

        try:
            self.output_file_path = d['simulation']['output-path']
        except KeyError:
            self.output_file_path = os.path.join(os.getcwd(), 'out.csv')

        try:
            self.load_convergence_tolerance = d['simulation']['load convergence tolerance']
        except KeyError:
            self.load_convergence_tolerance = 0.1

        self.drive_sim_with_inlet_temps = False
        try:
            if d['simulation']['plant driver'] == 'inlet-flow':
                self.drive_sim_with_inlet_temps = True
        except KeyError:
            pass

        if self.drive_sim_with_inlet_temps:
            self.inlet_temp_profile = make_inlet_temp_profile(d['flow-profile'])
        else:
            self.load_profile = make_load_profile(d['load-profile'])

        self.flow_profile = make_flow_profile(d['flow-profile'])

        self.glhe_entering_fluid_temperature = self.g.my_ground_temp(time=0, depth=50)
        self.response = TimeStepSimulationResponse(outlet_temp=self.glhe_entering_fluid_temperature)

        # plant fluids instance
        self.fluid = Fluid(d['fluid'])

        # other inits
        self.sim_time = 0
        self.current_load = 0
        self.mass_flow_rate = 0
        self.fluid_cap = 0
        self.print_idx = 0
        self.init_output_vars = True

    def report_output(self):
        ret_vals = {"Simulation Time": self.sim_time,
                    "Plant Load [W]": self.current_load,
                    "Plant Mass Flow Rate [kg/s]": self.mass_flow_rate,
                    "GLHE Inlet Temperature [C]": self.glhe_entering_fluid_temperature,
                    "GLHE Heat Transfer Rate [W]": self.response.heat_rate,
                    "GLHE Outlet Temperature [C]": self.response.outlet_temp}

        return ret_vals

    def simulate(self):
        start_time = datetime.datetime.now()

        try:
            if self.init_output_vars:
                self.init_output_vars = False

            while self.sim_time < self.run_time:

                if self.print_idx == 50:
                    print("Sim Time: {}".format(self.sim_time + gv.time_step))
                    self.print_idx = 0
                else:
                    self.print_idx += 1

                mean_temp = (self.glhe_entering_fluid_temperature + self.response.outlet_temp) / 2
                self.mass_flow_rate = self.flow_profile.get_value(self.sim_time)
                self.fluid_cap = self.mass_flow_rate * self.fluid.calc_specific_heat(mean_temp)

                if self.drive_sim_with_inlet_temps:

                    self.glhe_entering_fluid_temperature = self.inlet_temp_profile.get_value(self.sim_time)
                    new_response = self.g.simulate_time_step(self.glhe_entering_fluid_temperature,
                                                             self.mass_flow_rate,
                                                             gv.time_step,
                                                             True,
                                                             True)

                else:

                    self.current_load = self.load_profile.get_value(self.sim_time)
                    self.glhe_entering_fluid_temperature = self.response.outlet_temp + self.current_load / self.fluid_cap

                    # run manually to init the methods
                    self.g.simulate_time_step(self.glhe_entering_fluid_temperature,
                                              self.mass_flow_rate,
                                              gv.time_step,
                                              True,
                                              False)

                    # find result
                    res = minimize(self.wrapped_sim_time_step,
                                   x0=self.glhe_entering_fluid_temperature,
                                   method='Nelder-Mead',
                                   options={'fatol': self.load_convergence_tolerance})

                    # set result
                    self.glhe_entering_fluid_temperature = res.x[0]

                    # run manually one more time to lock down state
                    new_response = self.g.simulate_time_step(self.glhe_entering_fluid_temperature,
                                                             self.mass_flow_rate,
                                                             gv.time_step,
                                                             False,
                                                             True)

                self.response.outlet_temp = new_response.outlet_temp
                self.response.heat_rate = new_response.heat_rate
                self.op.collect_output([self.report_output(), self.g.report_output()])

                self.sim_time += gv.time_step

            # dump the results to a file
            self.op.write_to_file(self.output_file_path)

            log_file = '{}{}'.format(self.output_file_path.split('.csv')[0], '.log')

            with open(log_file, 'w') as f:
                f.write('Final runtime: {}'.format(datetime.datetime.now() - start_time))

            print('Final runtime: {}'.format(datetime.datetime.now() - start_time))

        except SimulationError:  # pragma: no cover
            raise SimulationError('Program failed')  # pragma: no cover

    def wrapped_sim_time_step(self, input_args):
        ret_response = self.g.simulate_time_step(input_args[0],
                                                 self.mass_flow_rate,
                                                 gv.time_step,
                                                 False,
                                                 False)

        # load = self.fluid_cap * (input_args[0] - ret_response.outlet_temp)
        # return abs(load - self.current_load)
        return abs(ret_response.heat_rate - self.current_load)


if __name__ == '__main__':
    RunGFunctions(sys.argv[1]).simulate()
