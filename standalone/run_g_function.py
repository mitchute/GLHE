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
from glhe.outputProcessor.processor import op
from glhe.profiles.factory_flow import make_flow_profile
from glhe.profiles.factory_load import make_load_profile
from glhe.properties.fluid import Fluid


class RunGFunctions(object):
    def __init__(self, input_file):

        # get input from file
        d = InputProcessor().process_input(input_file)

        # set the global level time-step
        gv.time_step = set_time_step(d['simulation']['time-steps per hour'])

        # init the g-function object and resister the output variables after init
        self.g = GFunction(d)
        self.g.register_output_variables()

        self.run_time = d['simulation']['runtime']

        try:
            self.output_file_path = d['simulation']['output path']
        except KeyError:
            self.output_file_path = os.getcwd()

        try:
            self.load_convergence_tolerance = d['simulation']['load convergence tolerance']
        except KeyError:
            self.load_convergence_tolerance = 0.1

        self.load_profile = make_load_profile(d['load-profile'])
        self.flow_profile = make_flow_profile(d['flow-profile'])

        self.glhe_entering_fluid_temperature = d['simulation']['initial-fluid-temperature']
        self.response = TimeStepSimulationResponse(outlet_temperature=self.glhe_entering_fluid_temperature)

        # plant fluids instance
        self.fluid = Fluid(d['fluid'])

        # other inits
        self.sim_time = 0
        self.current_load = 0
        self.mass_flow_rate = 0
        self.print_idx = 0
        self.init_output_vars = True

    def register_output_variables(self):
        op.register_output_variable(self, 'sim_time', "Simulation Time")
        op.register_output_variable(self, 'current_load', "Plant Load [W]")
        op.register_output_variable(self, 'mass_flow_rate', "Plant Mass Flow Rate [kg/s]")
        op.register_output_variable(self, 'glhe_entering_fluid_temperature', "GLHE Inlet Temperature [C]")
        op.register_output_variable(self.response, 'heat_rate', "GLHE Heat Transfer Rate [W]")
        op.register_output_variable(self.response, 'outlet_temperature', "GLHE Outlet Temperature [C]")

    def simulate(self):
        start_time = datetime.datetime.now()

        try:
            if self.init_output_vars:
                self.register_output_variables()
                self.init_output_vars = False

            while self.sim_time < self.run_time:

                # only print every so often
                if self.print_idx == 50:
                    print("Sim Time: {}".format(self.sim_time))
                    self.print_idx = 0
                else:
                    self.print_idx += 1

                # set current plant status
                self.current_load = self.load_profile.get_value(self.sim_time)
                self.mass_flow_rate = self.flow_profile.get_value(self.sim_time)

                # update entering fluid temperature
                mean_temp = (self.glhe_entering_fluid_temperature + self.response.outlet_temperature) / 2
                cp = self.fluid.calc_specific_heat(mean_temp)
                eft_num = self.current_load
                eft_den = self.mass_flow_rate * cp
                self.glhe_entering_fluid_temperature = self.response.outlet_temperature + eft_num / eft_den

                # run manually to init the methods
                self.g.simulate_time_step(self.glhe_entering_fluid_temperature,
                                          self.mass_flow_rate,
                                          True,
                                          False)

                # find result
                res = minimize(self.wrapped_sim_time_step,
                               x0=self.glhe_entering_fluid_temperature,
                               method='Nelder-Mead',
                               options={'fatol': self.load_convergence_tolerance})

                # set result
                self.glhe_entering_fluid_temperature = res.x

                # run manually one more time to lock down state
                new_response = self.g.simulate_time_step(self.glhe_entering_fluid_temperature,
                                                         self.mass_flow_rate,
                                                         False,
                                                         True)

                self.response.heat_rate = new_response.heat_rate
                self.response.outlet_temperature = new_response.outlet_temperature

                # update the output variables
                op.report_output()

                # advance in time through the GLHE for the next time step
                self.sim_time += gv.time_step

            # dump the results to a file
            op.write_to_file(os.path.join(self.output_file_path, 'out.csv'))
            print('Final runtime: {}'.format(datetime.datetime.now() - start_time))
        except SimulationError:  # pragma: no cover
            raise SimulationError('Program failed')  # pragma: no cover

    def wrapped_sim_time_step(self, inlet_temp):
        ret_response = self.g.simulate_time_step(inlet_temp,
                                                 self.mass_flow_rate,
                                                 False,
                                                 False)

        return abs(ret_response.heat_rate - self.current_load)


if __name__ == '__main__':
    RunGFunctions(sys.argv[1]).simulate()
