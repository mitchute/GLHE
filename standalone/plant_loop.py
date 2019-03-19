#!/usr/bin/env python3

import os
import sys
from typing import Union

from glhe.globals.functions import merge_dicts
from glhe.globals.functions import num_ts_per_hour_to_sec_per_ts
from glhe.input_processor.component_factory import make_component
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
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
            self.collect_outputs(end_of_this_time_step)
            current_sim_time = end_of_this_time_step

            if end_of_this_time_step >= self.end_sim_time:
                break

        self.op.write_to_file()

    def do_one_time_step(self, current_sim_time: Union[int, float]):
        """
        Simulate one time step of the entire plant loop
        """

        response = SimulationResponse(current_sim_time, self.time_step, 0, self.demand_inlet_temperature)

        for comp in self.demand_comps:
            response = comp.simulate_time_step(response)

    def report_outputs(self):

        d = {'Demand Inlet Temperature': self.demand_inlet_temperature,
             'Demand Outlet Temperature': self.demand_outlet_temperature,
             'Supply Inlet Temperature': self.supply_inlet_temperature,
             'Supply Outlet Temperature': self.supply_outlet_temperature}

        return d

    def collect_outputs(self, sim_time):

        d = {'Time': sim_time}

        d = merge_dicts(d, self.report_outputs())

        for comp in self.supply_comps:
            d = merge_dicts(d, comp.report_outputs())

        for comp in self.demand_comps:
            d = merge_dicts(d, comp.report_outputs())

        self.op.collect_output(d)


if __name__ == "__main__":
    PlantLoop(sys.argv[1]).simulate()
