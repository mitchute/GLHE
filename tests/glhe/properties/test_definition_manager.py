import unittest

from glhe.properties.definition_manager import DefinitionsMGR


class TestDefMgr(unittest.TestCase):

    @staticmethod
    def add_instance():
        d = {
            "borehole-definitions": [{
                "name": "borehole type 1",
                "depth": 100,
                "diameter": 0.1099,
                "grout-type": "standard grout",
                "model": "simple",
                "pipe-type": "32 mm SDR-11 HDPE",
                "segments": 10,
                "shank-spacing": 0.0521
            }],
            "grout-definitions": [{
                "name": "standard grout",
                "conductivity": 0.744,
                "density": 1500,
                "specific heat": 800
            }],
            "pipe-definitions": [
                {
                    "name": "26 mm SDR-11 HDPE",
                    "outer diameter": 0.0267,
                    "inner diameter": 0.0218,
                    "conductivity": 0.39,
                    "density": 950,
                    "specific heat": 1900
                }
            ]
        }

        def_mgr = DefinitionsMGR()
        def_mgr.load_definitions(d)
        return def_mgr

    def test_init(self):
        def_mgr = self.add_instance()

        self.assertEqual(len(def_mgr.borehole_defs), 1)
        self.assertEqual(len(def_mgr.grout_defs), 1)
        self.assertEqual(len(def_mgr.pipe_defs), 1)

    def test_get_borehole_definition(self):
        def_mgr = self.add_instance()
        bh_def = def_mgr.get_definition('borehole', 'borehole type 1')
        self.assertEqual(bh_def['name'], 'borehole type 1')

    def test_get_grout_definition(self):
        def_mgr = self.add_instance()
        grout_def = def_mgr.get_definition('grout', 'standard grout')
        self.assertEqual(grout_def['name'], 'standard grout')

    def test_get_pipe_definition(self):
        def_mgr = self.add_instance()
        pipe_def = def_mgr.get_definition('pipe', '26 mm SDR-11 HDPE')
        self.assertEqual(pipe_def['name'], '26 mm SDR-11 HDPE')

    def test_fail_def(self):
        def_mgr = self.add_instance()
        self.assertRaises(KeyError, def_mgr.get_definition, 'borehole', 'not a borehole name')
