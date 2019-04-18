from glhe.input_processor.component_types import ComponentTypes
from glhe.output_processor.report_types import ReportTypes


class SingleUTubePassThroughSegment(object):
    Type = ComponentTypes.SegmentSingleUTubeGrouted

    def __init__(self, inputs, ip, op):
        self.name = 'Seg No. {}'.format(inputs['segment-number'])
        self.ip = ip
        self.op = op

        # report variables
        self.temperature = ip.init_temp()

    def get_outlet_1_temp(self):
        return self.temperature

    def get_outlet_2_temp(self):
        return self.temperature

    def simulate_time_step(self, _, inputs: dict):
        self.temperature = inputs['inlet-1-temp']

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.temperature}
