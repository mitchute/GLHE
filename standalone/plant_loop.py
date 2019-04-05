#!/usr/bin/env python3

import os
import sys
from typing import Union

from glhe.globals.functions import merge_dicts
from glhe.globals.functions import num_ts_per_hour_to_sec_per_ts
from glhe.input_processor.component_factory import make_component
from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor


class PlantLoop(object):
    Type = ComponentTypes.PlantLoop

    def __init__(self, json_file_path: str) -> None:
        """
        Initialize the plant loop and all components on it.

        :param json_file_path: Path to the JSON input file
        """

        # process inputs
        self.ip = InputProcessor(json_file_path)

        # setup output processor
        try:
            self.op = OutputProcessor(self.ip.input_dict['simulation']['output-path'],
                                      self.ip.input_dict['simulation']['output-csv-name'])
        except KeyError:
            self.op = OutputProcessor(os.getcwd(), 'out.csv')

        # init plant-level variables
        self.demand_inlet_temp = self.ip.input_dict['simulation']['initial-temperature']
        self.demand_outlet_temp = self.ip.input_dict['simulation']['initial-temperature']
        self.supply_inlet_temp = self.ip.input_dict['simulation']['initial-temperature']
        self.supply_outlet_temp = self.ip.input_dict['simulation']['initial-temperature']
        self.end_sim_time = self.ip.input_dict['simulation']['runtime']
        self.time_step = num_ts_per_hour_to_sec_per_ts(self.ip.input_dict['simulation']['time-steps-per-hour'])
        self.demand_comps = []
        self.supply_comps = []

        # initialize plant loop components
        self.initialize_plant_loop_topology()

        # log initial conditions
        self.collect_outputs(0)

    def initialize_plant_loop_topology(self) -> None:

        for comp in self.ip.input_dict['topology']['supply-side']:
            self.supply_comps.append(make_component(comp, self.ip, self.op))

        for comp in self.ip.input_dict['topology']['demand-side']:
            self.demand_comps.append(make_component(comp, self.ip, self.op))

    def simulate(self) -> None:
        """
        Do the entire time stepping simulation of the plant loop
        """

        current_sim_time = 0

        while True:
            self.do_one_time_step(current_sim_time, self.time_step)
            current_sim_time += self.time_step
            self.collect_outputs(current_sim_time)

            if current_sim_time >= self.end_sim_time:
                break

        self.op.write_to_file()

    def do_one_time_step(self, current_sim_time: Union[int, float], time_step: Union[int, float]):
        """
        Simulate one time step of the entire plant loop
        """

        # update demand inlet node and initial conditions
        self.demand_inlet_temp = self.supply_outlet_temp
        response = SimulationResponse(current_sim_time, time_step, 0, self.demand_inlet_temp)

        # simulate demand components flow-wise
        for comp in self.demand_comps:
            response = comp.simulate_time_step(response)

        # update interface nodes
        self.demand_outlet_temp = response.temperature
        self.supply_inlet_temp = response.temperature

        # simulate supply components flow-wise
        for comp in self.supply_comps:
            response = comp.simulate_time_step(response)

        # supply outlet node
        self.supply_outlet_temp = response.temperature

    def report_outputs(self):

        d = {'{:s}:{:s}'.format(self.Type, 'Demand Inlet Temp. [C]'): self.demand_inlet_temp,
             '{:s}:{:s}'.format(self.Type, 'Demand Outlet Temp. [C]'): self.demand_outlet_temp,
             '{:s}:{:s}'.format(self.Type, 'Supply Inlet Temp. [C]'): self.supply_inlet_temp,
             '{:s}:{:s}'.format(self.Type, 'Supply Outlet Temp. [C]'): self.supply_outlet_temp}

        return d

    def collect_outputs(self, sim_time):

        # record current time
        d = {'Time': sim_time}

        # report outputs from the PlantLoop object
        d = merge_dicts(d, self.report_outputs())

        # collect reports from demand components
        for comp in self.demand_comps:
            d = merge_dicts(d, comp.report_outputs())

        # collect outputs from the supply components
        for comp in self.supply_comps:
            d = merge_dicts(d, comp.report_outputs())

        # finalize collection by by the OutputProcessor
        self.op.collect_output(d)


if __name__ == "__main__":
    PlantLoop(sys.argv[1]).simulate()
