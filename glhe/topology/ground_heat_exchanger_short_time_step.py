from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor


class GroundHeatExchangerSTS(SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        self.paths = []
        self.ip = ip
        self.op = op
        # self.fluid = ip.props_mgr.fluid
        # self.soil = ip.props_mgr.soil
        # self.gnd_temp = ip.gtm.get_temp
        #
        # init_temp = self.gnd_temp(0, 100)
        # self.inlet_temp = init_temp
        # self.outlet_temp = init_temp
        #
        # for path in inputs["paths"]:
        #     self.paths.append(Path(merge_dicts(path, {'initial temp': init_temp}), ip, op))

    def simulate_time_step(self, inputs: SimulationResponse):
        return inputs

    def report_outputs(self):
        pass

    # def set_flow_rates(self, plant_mass_flow_rate):
    #     for path in self.paths:
    #         path.set_flow_resistance()
    #
    #     self.delta_p_path = minimize_scalar(self.calc_total_mass_flow_from_delta_p, args=plant_mass_flow_rate,
    #                                         method='Golden', bracket=(0, self.delta_p_path), bounds=(0, 10e7),
    #                                         tol=0.01).x
    #
    #     for i, path in enumerate(self.paths):
    #         path.set_mass_flow_rate(sqrt(self.delta_p_path / path.flow_resistance))
    #
    # def calc_total_mass_flow_from_delta_p(self, delta_p, plant_mass_flow_rate):
    #     path_mass_flow = []
    #     for i, path in enumerate(self.paths):
    #         path_mass_flow.append(sqrt(delta_p / path.flow_resistance))
    #     return abs(plant_mass_flow_rate - sum(path_mass_flow))

    # def simulate_time_step(self, time, time_step, ):
    #     import random
    #     return 18 + float(random.randint(1, 100)) / 50
    # self.inlet_temp = plant_inlet_temperature
    # self.fluid.update_properties(mean([self.inlet_temp, self.outlet_temp]))
    # self.set_flow_rates(plant_mass_flow_rate)
    #
    # for path in self.paths:
    #     path.simulate(self.inlet_temp)
