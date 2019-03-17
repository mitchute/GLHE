from abc import ABCMeta
from typing import Union

import numpy as np

from glhe.input_processor.input_processor import InputProcessor
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.output_processor import OutputProcessor
from glhe.profiles.base_load import BaseLoad


class SyntheticBase(BaseLoad):
    """
    Pinel, P. 2003. 'Amelioration, Validation et Implantation _d'un Algorithme
    de Calcul pour Evaluer le Transfert Thermique Dans les Puits Verticaux de
    Systemes de Pompes a Chaleur'
    Geothermiques. M.S.Sc. Thesis. Ecole Polytechnique Montreal

    ** Bernier, M.A., Labib, R., Pinel, P., and Paillot, R. 2004. 'A multiple
    load aggregation algorithm for annual hourly simulations of GCHP systems.'
    HVAC&R Research, 10(4): 471-487.

    ** Equation is referenced here, but it has typos
    """

    __metaclass__ = ABCMeta

    def __init__(self, inputs):
        BaseLoad.__init__(self)
        self._a = inputs["a"]
        self._b = inputs["b"]
        self._c = inputs["c"]
        self._d = inputs["d"]
        self._e = inputs["e"]
        self._f = inputs["f"]
        self._g = inputs["g"]

    def q_1(self, t):
        term_1 = self._a * np.sin(np.pi * (t - self._b) / 12)
        term_2 = np.sin(self._f * np.pi * (t - self._b) / 8760)

        result = term_1 * term_2

        return result

    def q_2(self, t):
        term_1 = (168 - self._c) / 168
        term_2 = 0.0
        for i in range(1, 4):
            term_2 += (np.cos(i * np.pi * self._c / 84) - 1) * \
                      (np.sin(i * np.pi * (t - self._b) / 84)) / (i * np.pi)

        result = term_1 + term_2

        return result

    def floor(self, t):
        result = np.floor(self._f * (t - self._b) / 8760)

        return result

    def signum(self, t):
        term_1 = np.cos(self._f * np.pi * (t - self._g) / 4380) + self._e

        if term_1 >= 0:
            return 1
        else:
            return -1

    def get_value(self, time):
        q_1 = self.q_1(time)
        q_2 = self.q_2(time)
        floor = self.floor(time)
        sig_num = self.signum(time)
        return (q_1 * q_2) + pow(-1.0, floor) * np.abs(q_1 * q_2) + self._d * pow(-1.0, floor) * sig_num


class SyntheticLoad(SyntheticBase, SimulationEntryPoint):

    def __init__(self, inputs: dict, ip: InputProcessor, op: OutputProcessor):
        self.ip = ip
        self.op = op

        if inputs['synthetic-method'] == 'asymmetric':
            params = {'a': inputs['amplitude'],
                      'b': 1000,
                      'c': 80,
                      'd': 0.01,
                      'e': 0.95,
                      'f': 4 / 3,
                      'g': 2190}
            SyntheticBase.__init__(self, params)
        elif inputs['synthetic-method'] == 'symmetric':
            params = {'a': inputs['amplitude'],
                      'b': 2190,
                      'c': 80,
                      'd': 0.01,
                      'e': 0.95,
                      'f': 2,
                      'g': 0}
            SyntheticBase.__init__(self, params)
        else:
            raise ValueError("Synthetic method '{}' is not valid.".format(type))

    def simulate_time_step(self, sim_time: Union[int, float], time_step: Union[int, float],
                           mass_flow_rate: Union[int, float], inlet_temp: Union[int, float]):
        load = self.get_value(sim_time)
        specific_heat = self.ip.props_mgr.fluid.get_cp()
        outlet_temp = load / (mass_flow_rate * specific_heat) + inlet_temp
        return SimulationResponse(sim_time, time_step, mass_flow_rate, outlet_temp)
