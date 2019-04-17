import numpy as np

from glhe.globals.functions import merge_dicts
from glhe.globals.functions import runge_kutta_fourth_y
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.properties.base_properties import PropertiesBase
from glhe.topology.pipe import Pipe


class SingleUTubeGroutedSegment(SimulationEntryPoint):
    Type = ComponentTypes.SegmentSingleUTubeGrouted

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs['segment-number'])
        self.ip = ip
        self.op = op

        self.fluid = ip.props_mgr.fluid
        self.soil = ip.props_mgr.soil
        self.grout = PropertiesBase(ip.get_definition_object('grout-definitions', bh_def_inputs['grout-def-name']))

        self.num_pipes = 2
        self.length = inputs['length']
        self.diameter = inputs['diameter']

        self.pipe_1 = Pipe(merge_dicts(inputs['pipe-data'], {'length': self.length,
                                                             'initial temp': inputs['initial temp']}),
                           fluid_inst=fluid_inst)

        self.pipe_2 = Pipe(merge_dicts(inputs['pipe-data'], {'length': self.length,
                                                             'initial temp': inputs['initial temp']}),
                           fluid_inst=fluid_inst)

        self.num_equations = 4
        self.y = np.full((self.num_equations,), ip.init_temp())

        self.borehole_wall_temp = ip.init_temp()
        self.inlet_temp_1 = ip.init_temp()
        self.inlet_temp_2 = ip.init_temp()

        self.mass_flow_rate = 0
        self.bh_resist = 0
        self.direct_coupling_resist = 0

    def right_hand_side(self, y):
        num_equations = 4
        r = np.zeros(num_equations)

        dz = self.length
        t_b = self.borehole_wall_temp
        t_i_1 = self.inlet_temp_1
        t_i_2 = self.inlet_temp_2

        r_f = 1 / (self.mass_flow_rate * self.fluid.specific_heat)
        r_b = self.bh_resist
        r_12 = self.direct_coupling_resist

        c_f_1 = self.fluid.heat_capacity * self.pipe_1.fluid_vol
        c_f_2 = self.fluid.heat_capacity * self.pipe_2.fluid_vol

        # spilt between inner and outer grout layer
        f = 0.1
        c_g_1 = f * self.grout.specific_heat * self.grout.density * self.GROUT_VOL
        c_g_1 += self.pipe_1.specific_heat * self.pipe_1.density * self.pipe_1.pipe_wall_vol

        c_g_2 = (1 - f) * self.grout.specific_heat * self.grout.density * self.GROUT_VOL
        c_g_2 += self.pipe_2.specific_heat * self.pipe_2.density * self.pipe_2.pipe_wall_vol

        r[0] = ((t_i_1 - y[0]) / r_f + (y[2] - y[0]) * dz / (r_12 / 2.0) + (y[3] - y[0]) * dz / r_b) / c_f_1
        r[1] = ((t_i_2 - y[1]) / r_f + (y[2] - y[1]) * dz / (r_12 / 2.0) + (y[3] - y[1]) * dz / r_b) / c_f_2
        r[2] = ((y[0] - y[2]) * dz / (r_12 / 2.0) + (y[1] - y[2]) * dz / (r_12 / 2.0)) / c_g_1
        r[3] = ((y[0] - y[3]) * dz / r_b + (y[1] - y[3]) * dz / r_b + (t_b - y[3]) * dz / (r_b / 2.0)) / c_g_2

        return r

    def simulate(self, timestep, **kwargs):
        self.borehole_wall_temp = kwargs['borehole wall temp']
        self.inlet_temp_1 = kwargs['inlet 1 temp']
        self.inlet_temp_2 = kwargs['inlet 2 temp']

        self.mass_flow_rate = kwargs['mass flow rate']
        self.bh_resist = kwargs['borehole resistance']
        self.direct_coupling_resist = kwargs['direct coupling resistance']

        self.y = runge_kutta_fourth_y(self.right_hand_side, timestep, y=self.y)
        return self.y

    def get_outlet_1_temp(self):
        return self.y[0]

    def get_outlet_2_temp(self):
        return self.y[1]

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        pass

    def report_outputs(self) -> dict:
        pass
