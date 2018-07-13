import sys

from glhe.gFunction.main import GFunction
from glhe.globals.functions import set_time_step
from glhe.inputProcessor.processor import InputProcessor
from glhe.interface.response import TimeStepSimulationResponse
from glhe.profiles.factory_flow import make_flow_profile
from glhe.profiles.factory_load import make_load_profile
from glhe.properties.fluid import Fluid


def main(input_file):
    d = InputProcessor().process_input(input_file)

    g = GFunction(d)

    time_step = set_time_step(d['simulation']['time-step'])
    run_time = d['simulation']['runtime']

    load_profile = make_load_profile(d['load-profile'])
    flow_profile = make_flow_profile(d['flow-profile'])

    glhe_entering_fluid_temperature = d['simulation']['initial-fluid-temperature']
    response = TimeStepSimulationResponse(outlet_temperature=glhe_entering_fluid_temperature)

    # plant fluids instance
    fluid = Fluid(d['fluid'])

    time = 0
    while time <= run_time:
        # advance in time through the GLHE
        time += time_step

        # set current plant status
        current_load = load_profile.get_value(time)
        mass_flow_rate = flow_profile.get_value(time)

        # update entering fluid temperature
        cp = fluid.calc_specific_heat((glhe_entering_fluid_temperature + response.outlet_temperature) / 2)
        glhe_entering_fluid_temperature = response.outlet_temperature + current_load / (mass_flow_rate * cp)

        # compute glhe response
        response = g.simulate_time_step(glhe_entering_fluid_temperature, mass_flow_rate, time_step)


if __name__ == '__main__':
    main(sys.argv[1])
