from glhe.functions import init_temp, get_definition_object
from glhe.simulation import SimulationEntryPoint, SimulationResponse
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole
from glhe.topology.pipe import Pipe


class Path(SimulationEntryPoint):

    def __init__(self, all_inputs: dict, ghe_inputs: dict):
        SimulationEntryPoint.__init__(self, all_inputs)

        # valid components which can exist on the path
        valid_comp_types = ['borehole', 'pipe']

        # init all components on the path
        self.components = []
        for comp in ghe_inputs['components']:
            comp_type = comp['comp-type']
            assert comp_type in valid_comp_types
            comp_name = comp['name']
            if comp_type == 'pipe':
                inputs = get_definition_object(ghe_inputs, comp_type, comp_name)
                self.components.append(Pipe(inputs))
            elif comp_type == 'borehole':
                bh_name = comp['name']
                if 'average-borehole' not in ghe_inputs:
                    comp_inputs = get_definition_object(all_inputs, 'borehole', bh_name)
                    def_inputs = get_definition_object(all_inputs, 'borehole-definitions', comp_inputs['borehole-def-name'])
                    bh_type = def_inputs['borehole-type']
                else:
                    bh_type = ghe_inputs['borehole-type']
                assert(bh_type == 'single-grouted')
                self.components.append(SingleUTubeGroutedBorehole(all_inputs, ghe_inputs))

        # report variables
        self.inlet_temperature = init_temp()
        self.outlet_temperature = init_temp()
        self.flow_rate = 0

    def get_heat_rate_bh(self) -> float:
        bh_ht_rate = 0
        for comp in self.components:
            if hasattr(comp, 'get_heat_rate_bh'):
                bh_ht_rate += comp.get_heat_rate_bh()
        return bh_ht_rate

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:

        if inputs.bh_wall_temp:
            response = SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, inputs.temperature,
                                          inputs.bh_wall_temp)
        else:
            response = SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, inputs.temperature)

        for comp in self.components:
            response = comp.simulate_time_step(response)

        # update report variables
        self.flow_rate = inputs.flow_rate
        self.inlet_temperature = inputs.temperature
        self.outlet_temperature = response.temperature
        return response
