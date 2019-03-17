import os
import tempfile
import unittest

from glhe.gFunction.g_function import GFunction
from glhe.globals.functions import num_ts_per_hour_to_sec_per_ts
from glhe.globals.functions import write_json
from glhe.globals.variables import gv
from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint


class TestGFunction(unittest.TestCase):

    @staticmethod
    def add_instance(file_number=0, depth=100):

        temp_directory = tempfile.mkdtemp()
        temp_g_function_file = os.path.join(temp_directory, 'g_funcs.csv')
        if file_number == 1:
            with open(temp_g_function_file, 'w') as f:
                f.write('-12.669987, -0.560985\n')
                f.write('-12.535471, -0.425707\n')
                f.write('-12.400955, -0.290607\n')
                f.write('-12.26644, -0.15656\n')
                f.write('-12.131924, -0.024406\n')
                f.write('-11.997408, 0.105089\n')
        else:
            with open(temp_g_function_file, 'w') as f:
                f.write('1, 1\n2, 2\n3, 3\n')

        d = {
            "borehole-definitions": [
                {
                    "name": "borehole type 1",
                    "depth": 100,
                    "diameter": 0.114,
                    "grout-type": "standard grout",
                    "model": "single",
                    "pipe-type": "32 mm SDR-11 HDPE",
                    "segments": 10,
                    "shank-spacing": 0.0469
                }
            ],
            "flow-profile": {
                "type": "fixed",
                "fixed": {
                    "value": 0.2
                }
            },
            "fluid": {
                "type": "water",
                "concentration": 100
            },
            "g-functions": {
                "file": temp_g_function_file,
                "borehole-type": "borehole type 1",
                "number of boreholes": 1
            },
            "ground-temperature": {
                "type": "constant",
                "constant": {
                    "temperature": 20
                }
            },
            "grout-definitions": [
                {
                    "name": "standard grout",
                    "conductivity": 0.744,
                    "density": 1500,
                    "specific heat": 800
                }
            ],
            "load-aggregation": {
                "type": "none"
            },
            "pipe-definitions": [
                {
                    "name": "32 mm SDR-11 HDPE",
                    "outer diameter": 0.0334,
                    "inner diameter": 0.0269,
                    "conductivity": 0.389,
                    "density": 950,
                    "specific heat": 1900
                }
            ],
            "soil": {
                "name": "Some Rock",
                "conductivity": 2.6,
                "density": 1500,
                "specific heat": 1000
            }
        }

        d['borehole-definitions'][0]['depth'] = depth

        temp_file = os.path.join(temp_directory, 'temp.json')
        write_json(temp_file, d)
        inputs = InputProcessor().process_input(temp_file)
        g = GFunction(inputs=inputs)
        return g

    def test_class_inheritance(self):
        tst = self.add_instance()
        self.assertIsInstance(tst, SimulationEntryPoint)

    def test_init_a(self):
        self.add_instance()

    def test_g_function_interp(self):
        tst = self.add_instance()
        self.assertEqual(tst.g_function_interp(0.5), 0.5)
        self.assertEqual(tst.g_function_interp(1.5), 1.5)
        self.assertEqual(tst.g_function_interp(2.5), 2.5)
        self.assertEqual(tst.g_function_interp(3.5), 3.5)

    def test_get_g_func(self):
        tst = self.add_instance()
        self.assertAlmostEqual(tst.get_g_func(1742488352), 1.0, delta=0.000001)
        self.assertAlmostEqual(tst.get_g_func(4736574422), 2.0, delta=0.000001)
        self.assertAlmostEqual(tst.get_g_func(12875344180), 3.0, delta=0.000001)

    def test_simulate_time_step(self):
        tst = self.add_instance(file_number=1)
        gv.time_step = num_ts_per_hour_to_sec_per_ts(1)
        ret_temp = tst.simulate_time_step(inlet_temp=20.0,
                                          mass_flow_rate=0,
                                          time_step=gv.time_step,
                                          first_pass=True,
                                          converged=False)
        self.assertEqual(ret_temp, 20.0)

        tst = self.add_instance(file_number=1)
        gv.time_step = num_ts_per_hour_to_sec_per_ts(1)
        ret_temp = tst.simulate_time_step(inlet_temp=25.0,
                                          mass_flow_rate=0.2,
                                          time_step=gv.time_step,
                                          first_pass=True,
                                          converged=True)
        self.assertAlmostEqual(ret_temp, 29.5, delta=0.1)

        tst = self.add_instance(file_number=1)
        gv.time_step = num_ts_per_hour_to_sec_per_ts(1)
        ret_temp = tst.simulate_time_step(inlet_temp=25.0,
                                          mass_flow_rate=0.2,
                                          time_step=gv.time_step,
                                          first_pass=True,
                                          converged=True)
        self.assertAlmostEqual(ret_temp, 29.5, delta=0.1)

        ret_temp = tst.simulate_time_step(inlet_temp=25.0,
                                          mass_flow_rate=0.2,
                                          time_step=gv.time_step,
                                          first_pass=True,
                                          converged=True)
        self.assertAlmostEqual(ret_temp, 22.8, delta=0.1)

        ret_temp = tst.simulate_time_step(inlet_temp=25.0,
                                          mass_flow_rate=0.2,
                                          time_step=gv.time_step,
                                          first_pass=True,
                                          converged=True)
        self.assertAlmostEqual(ret_temp, 23.1, delta=0.1)

        ret_temp = tst.simulate_time_step(inlet_temp=25.0,
                                          mass_flow_rate=0.2,
                                          time_step=gv.time_step,
                                          first_pass=True,
                                          converged=True)
        self.assertAlmostEqual(ret_temp, 23.3, delta=0.1)
