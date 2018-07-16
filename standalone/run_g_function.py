import sys

from glhe.gFunction.main import GFunction
from glhe.globals.functions import set_time_step
from glhe.inputProcessor.processor import InputProcessor
from glhe.interface.response import TimeStepSimulationResponse
from glhe.outputProcessor.processor import OutputProcessor
from glhe.profiles.factory_flow import make_flow_profile
from glhe.profiles.factory_load import make_load_profile
from glhe.properties.fluid import Fluid


class RunGFunctions(object):
    def __init__(self, input_file):
        # get input from file
        d = InputProcessor().process_input(input_file)
        self.g = GFunction(d)

        self.time_step = set_time_step(d['simulation']['time-step'])
        self.run_time = d['simulation']['runtime']

        self.load_profile = make_load_profile(d['load-profile'])
        self.flow_profile = make_flow_profile(d['flow-profile'])

        self.glhe_entering_fluid_temperature = d['simulation']['initial-fluid-temperature']
        self.response = TimeStepSimulationResponse(outlet_temperature=self.glhe_entering_fluid_temperature)

        self.sim_time = 0
        self.current_load = 0
        self.mass_flow_rate = 0

        # plant fluids instance
        self.fluid = Fluid(d['fluid'])

    def simulate(self):
        op = OutputProcessor()
        while self.sim_time <= self.run_time:
            # advance in time through the GLHE
            self.sim_time += self.time_step
            print("Sim Time: {}".format(self.sim_time))
            op.register_output_variable(self, 'sim_time', "Simulation Time")

            # set current plant status
            self.current_load = self.load_profile.get_value(self.sim_time)
            self.mass_flow_rate = self.flow_profile.get_value(self.sim_time)
            op.register_output_variable(self, 'current_load', "Plant Load [W]")
            op.register_output_variable(self, 'mass_flow_rate', "Plant Mass Flow Rate [kg/s]")

            # update entering fluid temperature
            mean_temp = (self.glhe_entering_fluid_temperature + self.response.outlet_temperature) / 2
            cp = self.fluid.calc_specific_heat(mean_temp)
            self.glhe_entering_fluid_temperature = self.response.outlet_temperature - self.current_load / (
                        self.mass_flow_rate * cp)
            op.register_output_variable(self, 'glhe_entering_fluid_temperature', "GLHE Inlet Temperature [C]")

            # compute glhe response
            self.response = self.g.simulate_time_step(self.glhe_entering_fluid_temperature, self.mass_flow_rate,
                                                      self.time_step)
            op.register_output_variable(self.response, 'heat_rate', "GLHE Heat Transfer Rate [W]")
            op.register_output_variable(self.response, 'outlet_temperature', "GLHE Outlet Temperature [C]")
            op.report_output()

        op.write_to_file('test.csv')


if __name__ == '__main__':
    RunGFunctions(sys.argv[1]).simulate()
