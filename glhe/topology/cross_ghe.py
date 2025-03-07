from glhe.aggregation.dynamic import Dynamic
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.external_base import ExternalBase
from glhe.functions import merge_dicts


class CrossGHE:
    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        try:  # pragma: no cover
            self.name = inputs['name'].upper()
        except KeyError:  # pragma: no cover
            pass  # pragma: no cover

        self.ip = ip
        self.op = op

        self.h = inputs['length']
        self.start_time = inputs['start-time']
        sim_time = ip.input_dict['simulation']['runtime']

        self.load_agg = Dynamic(
            merge_dicts(inputs['load-aggregation'], {'runtime': sim_time - self.start_time})
        )
        self.loads = ExternalBase(inputs['load-data-path'], col_num=0)

    def simulate_time_step(self, dt: float, time: float) -> None:
        agg_time = time + dt - self.start_time
        if agg_time > 0:
            energy = self.loads.get_value(agg_time) / self.h * dt
            self.load_agg.aggregate(agg_time, energy)
