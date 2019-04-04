import os
import tempfile
import unittest

from glhe.aggregation.agg_method_factory import make_agg_method
from glhe.globals.functions import write_json
from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor


class TestDynamic(unittest.TestCase):

    @staticmethod
    def add_instance():
        d_to_file = {'simulation': {'name': 'test dynamic',
                                    'initial-temperature': 16,
                                    'time-steps-per-hour': 60,
                                    'runtime': 36000}}

        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, 'temp.json')

        write_json(temp_file, d_to_file)

        ip = InputProcessor(temp_file)
        op = OutputProcessor(temp_dir, 'out.csv')
 
        d = {'method': 'dynamic', 'expansion-rate': 2, 'number-bins-per-level': 9}
        
        return make_agg_method(d, ip, op)

    def test_aggregate(self):

        tst = self.add_instance()

        delta_t = 3600
        time = 0

        tst.aggregate(time + delta_t, delta_t, 1)
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 0)

        time += delta_t
        tst.aggregate(time + delta_t, delta_t)
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 1)
        self.assertEqual(tst.loads[6].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 1.5)
        self.assertEqual(tst.loads[6].energy, 0.5)
        self.assertEqual(tst.loads[7].energy, 0)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 1.75)
        self.assertEqual(tst.loads[6].energy, 1.0)
        self.assertEqual(tst.loads[7].energy, 0.25)
        self.assertEqual(tst.loads[8].energy, 0.)

        tst.get_new_current_load_bin(width=gv.time_step)
        tst.set_current_load(1)
        tst.aggregate()
        self.assertEqual(tst.loads[0].energy, 1)
        self.assertEqual(tst.loads[1].energy, 1)
        self.assertEqual(tst.loads[2].energy, 1)
        self.assertEqual(tst.loads[3].energy, 1)
        self.assertEqual(tst.loads[4].energy, 1)
        self.assertEqual(tst.loads[5].energy, 1.875)
        self.assertEqual(tst.loads[6].energy, 1.375)
        self.assertEqual(tst.loads[7].energy, 0.625)
        self.assertEqual(tst.loads[8].energy, 0.125)
        self.assertEqual(tst.loads[9].energy, 0)
