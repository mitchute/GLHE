from glhe.input_processor.component_types import ComponentTypes
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes


class ConstantLoad(SimulationEntryPoint):
    Type = ComponentTypes.ConstantLoad

    def __init__(self, inputs: dict, ip: InputProcessor):
        SimulationEntryPoint.__init__(self, inputs)
        self.load = inputs['value']
        self.ip = ip

        # report variables
        self.inlet_temp = ip.init_temp()
        self.outlet_temp = ip.init_temp()

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        self.inlet_temp = inputs.temperature
        flow_rate = inputs.flow_rate

        if flow_rate == 0:
            return inputs

        specific_heat = self.ip.fluid.cp(self.inlet_temp)
        self.outlet_temp = self.load / (flow_rate * specific_heat) + self.inlet_temp
        return SimulationResponse(inputs.time, inputs.time_step, inputs.flow_rate, self.outlet_temp)

    def report_outputs(self):
        return {f"{self.Type}:{self.name}:{ReportTypes.InletTemp}": float(self.inlet_temp),
                f"{self.Type}:{self.name}:{ReportTypes.OutletTemp}": float(self.outlet_temp),
                f"{self.Type}:{self.name}:{ReportTypes.HeatRate}": float(self.load)}
