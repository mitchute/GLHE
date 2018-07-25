import datetime
import os
import sys

from glhe.gFunction.g_function import GFunction
from glhe.globals.functions import set_time_step
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
        self.g = GFunction(d)
        self.g.register_output_variables()

        self.time_step = set_time_step(d['simulation']['time-step'])
        self.run_time = d['simulation']['runtime']

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
        self.first_time = True

    def register_output_variables(self):
        op.register_output_variable(self, 'sim_time', "Simulation Time")
        op.register_output_variable(self, 'current_load', "Plant Load [W]")
        op.register_output_variable(self, 'mass_flow_rate', "Plant Mass Flow Rate [kg/s]")
        op.register_output_variable(self, 'glhe_entering_fluid_temperature', "GLHE Inlet Temperature [C]")
        op.register_output_variable(self.response, 'heat_rate', "GLHE Heat Transfer Rate [W]")
        op.register_output_variable(self.response, 'outlet_temperature', "GLHE Outlet Temperature [C]")

    def simulate(self):
        if self.first_time:
            self.register_output_variables()
            self.first_time = False

        while self.sim_time <= self.run_time:
            # advance in time through the GLHE
            self.sim_time += self.time_step

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

            # compute glhe response
            new_response = self.g.simulate_time_step(self.glhe_entering_fluid_temperature,
                                                     self.mass_flow_rate,
                                                     self.time_step)

            self.response.heat_rate = new_response.heat_rate
            self.response.outlet_temperature = new_response.outlet_temperature

            # update the output variables
            op.report_output()

        # dump the results to a file
        op.write_to_file('test.csv')


if __name__ == '__main__':
    print(sys.argv)
    start = datetime.datetime.now()
    if os.path.exists(sys.argv[1]):
        RunGFunctions(sys.argv[1]).simulate()
    else:
        FileNotFoundError("Input file: '{}' does not exist".format(sys.argv[1]))
    print('Final runtime: {}'.format(datetime.datetime.now() - start))
