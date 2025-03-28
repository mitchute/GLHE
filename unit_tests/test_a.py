from json import loads
from pathlib import Path
from unittest import TestCase

from glhe.simulation import SimulationResponse
from glhe.topology.ground_heat_exchanger import GroundHeatExchanger


class TestA(TestCase):
    def test_a(self):
        file = Path(__file__).resolve().parent.parent / "test_files" / "single.json"
        inputs = loads(file.read_text())
        ghe = GroundHeatExchanger(inputs, inputs['ground-heat-exchanger'][0])
        sim_time = 0
        time_step = 10
        inlet_temp = 20
        flow_rate = 0.5
        ghe_outlet_data = SimulationResponse(sim_time, time_step, flow_rate, inlet_temp)
        for _ in range(10):
            sim_time += time_step
            hp_t_out = ghe_outlet_data.temperature + 3
            heat_pump_outlet = SimulationResponse(sim_time, time_step, flow_rate, hp_t_out)
            ghe_outlet_data = ghe.simulate_time_step(heat_pump_outlet)
            print(f"HP_Tout: {hp_t_out}; GHE_Tout: {ghe_outlet_data.temperature}")