#!/usr/bin/env python3

import os
import sys

from glhe.globals.functions import num_ts_per_hour_to_sec_per_ts
from glhe.input_processor.component_factory import make_component
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor


class PlantLoop(object):

    def __init__(self, json_file_path: str) -> None:
        """
        Initialize the plant loop and all components on it.

        :param json_file_path: Path to the JSON input file
        :return None
        """

        # process inputs
        self.ip = InputProcessor(json_file_path)

        # setup output processor
        try:
            self.op = OutputProcessor(self.ip.inputs['simulation']['output-path'],
                                      self.ip.inputs['simulation']['output-csv-name'])
        except KeyError:
            self.op = OutputProcessor(os.getcwd(), 'out.csv')

        # init plant-level variables
        self.demand_inlet_temperature = self.ip.inputs['simulation']['initial-temperature']
        self.demand_outlet_temperature = self.ip.inputs['simulation']['initial-temperature']
        self.supply_inlet_temperature = self.ip.inputs['simulation']['initial-temperature']
        self.supply_outlet_temperature = self.ip.inputs['simulation']['initial-temperature']
        self.end_sim_time = self.ip.inputs['simulation']['runtime']
        self.time_step = num_ts_per_hour_to_sec_per_ts(self.ip.inputs['simulation']['time-steps-per-hour'])
        self.demand_comps = []
        self.supply_comps = []

        # initialize all of the plant loop components
        self.initialize_plant_loop_components()

    def initialize_plant_loop_components(self) -> None:

        for comp in self.ip.inputs['components']['supply-side']:
            self.supply_comps.append(make_component(comp, self.ip, self.op))

        for comp in self.ip.inputs['components']['demand-side']:
            self.demand_comps.append(make_component(comp, self.ip, self.op))

    def simulate(self) -> None:
        """
        Do the entire time stepping simulation of the plant loop
        """

        current_sim_time = 0
        while True:
            end_of_this_time_step = current_sim_time + self.time_step

            self.do_one_time_step(current_sim_time)

            if end_of_this_time_step >= self.end_sim_time:
                break

            current_sim_time = end_of_this_time_step

            self.op.collect_output({'Time': current_sim_time,
                                    'Demand Inlet Temperature': self.demand_inlet_temperature,
                                    'Demand Outlet Temperature': self.demand_outlet_temperature,
                                    'Supply Inlet Temperature': self.supply_inlet_temperature,
                                    'Supply Outlet Temperature': self.supply_outlet_temperature})

        self.op.write_to_file()

    def do_one_time_step(self, current_sim_time: int) -> bool:
        """
        Simulate one time step of the entire plant loop
        Consists of:
        
        - Adding a load
        - Looping over components
        
        :return: True if successful, False if not
        """

        self.flow_rate = self.flow_profile.get_value(current_sim_time)
        self.load = self.load_profile.get_value(current_sim_time)

        # Simulate demand side
        demand_cp = self.fluid.calc_specific_heat(self.demand_inlet_temperature)
        self.demand_outlet_temperature = self.demand_inlet_temperature + self.load / (self.flow_rate * demand_cp)
        # Simulate supply side
        self.supply_inlet_temperature = self.demand_outlet_temperature  # could do mass here?
        # TODO: Fix GLHE so we can call it
        import random
        self.supply_outlet_temperature = 18 + float(random.randint(1, 100)) / 50
        # self.supply_outlet_temperature = self.glhe.simulate_time_step(
        #     self.supply_inlet_temperature, self.flow_rate, current_sim_time
        # )
        # Advance time
        self.demand_inlet_temperature = self.supply_outlet_temperature  # could do mass here
        return True


if __name__ == "__main__":
    PlantLoop(sys.argv[1]).simulate()
