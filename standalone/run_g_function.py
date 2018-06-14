import json
import sys

from glhe.gFunction.main import GFunction
from glhe.profiles.factory import make_load_profile


def main():

    with open(sys.argv[1]) as f:
        json_blob = f.read()
    d = json.loads(json_blob)

    g = GFunction(d)

    time_step = d['simulation']['time-step']
    run_time = d['simulation']['runtime']

    load_profile = make_load_profile(d['simulation']['load-profile'])
    glhe_entering_fluid_temperature = d['simulation']['initial-fluid-temperature']

    mass_flow_rate = 1.0
    cp = 4180

    time = 0
    while time <= run_time:
        # advance in time through the GLHE
        time += time_step
        response = g.simulate_time_step(glhe_entering_fluid_temperature, mass_flow_rate, time_step)

        # update from the plant current conditions in preparation for the next time step
        current_load = load_profile.get_value(time)
        glhe_entering_fluid_temperature = response.outlet_temperature + current_load / (mass_flow_rate * cp)

        print(response.outlet_temperature)


if __name__ == '__main__':
    main()
