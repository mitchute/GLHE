import numpy as np

from glhe.globals.functions import lin_interp
from glhe.globals.functions import sec_to_hr
from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.external_base import ExternalBase
from glhe.properties.base_properties import PropertiesBase


class SwedishHP(PropertiesBase, SimulationEntryPoint):
    """
    Gehlin, Signhild E.A., Spitler, Jeffrey D. 2014. Design of residential ground source heat pump
    systems for heating dominated climates - trade-offs between ground heat exchanger design and
    supplementary electric resistance heating. ASHRAE Winter Conference. January 18-22. New York, NY.

    Implemented by MSM, after VBA code by JDS
    """

    Type = ComponentTypes.SwedishHP

    def __init__(self, inputs, ip, op):
        SimulationEntryPoint.__init__(self, inputs)

        # input/output processor
        self.ip = ip
        self.op = op

        # local fluids reference
        self.fluid = self.ip.props_mgr.fluid

        # input data
        self.max_htg_set_point = inputs['max-heating-set-point']
        self.min_htg_set_point = inputs['min-heating-set-point']
        self.wtr_htg_set_point = inputs['water-heating-set-point']
        self.odt_at_max_htg_set_point = inputs['outdoor-air-temperature-at-max-heating-set-point']
        self.odt_at_min_htg_set_point = inputs['outdoor-air-temperature-at-min-heating-set-point']
        self.imm_htr_capacity = inputs['immersion-heater-capacity']
        self.c_capacity = np.array(inputs['capacity-coefficients'])
        self.c_cop = np.array(inputs['coefficient-of-performance-coefficients'])
        self.htg_loads = ExternalBase(inputs['load-data-path'], 0)
        self.wtr_htg_loads = ExternalBase(inputs['load-data-path'], 1)
        self.oda_temps = ExternalBase(inputs['load-data-path'], 2)

        # report variables
        self.flow_rate = None
        self.inlet_temperature = None
        self.outlet_temperature = None

        # water heating report variables
        self.wtr_htg_elec = None  # electricity consumption of heat pump for water heating (kWh)
        self.wtr_htg_rtf = None  # run time fraction of heat pump (-)
        self.wtr_htg_imm_elec = None  # electricity consumption of immersion heater for water heating (kWh)
        self.wtr_htg_unmet = None  # unmet water heating load (kWh)

        # heating report variables
        self.htg_elec = None  # electricity consumption of heat pump for space heating (kWh)
        self.htg_rtf = None  # run time fraction of heat pump (-)
        self.htg_imm_elec = None  # electricity consumption of immersion heater for space heating (kWh)
        self.htg_unmet = None  # unmet water heating load (kWh)

        # other
        self.heat_extraction = None  # heat extracted from borehole (kWh)

    def x7_cop(self, src_side_eft, load_side_exft):
        """
        Gives COP the "X7" heat pump;
        data provided by Martin Forszn for an actual Swedish
        heat pump, but anonymized, so to speak.

        The capacity is for the vapor compression cycle only

        Input variables:

        src_side_eft: Source-side Entering Fluid Temperature(C)
           i.e. coming from ground heat exchanger
           will include some antifreeze
           Range +5 > src_side_eft > -5

        load_side_exft: Load-side Exiting Fluid Temperature(C)
            i.e. hot water going either to heat domestic hot water
            via double shell tank
            or to panel radiators

        Coefficients are derived using GLSQ
           Range +60 > load_side_exft > +35

        JDS 20130605

        :param src_side_eft: Source-side Entering Fluid Temperature(C)
        :param load_side_exft: Load-side Exiting Fluid Temperature(C)
        :return: COP
        """

        c_1 = self.c_cop[0]
        c_2 = self.c_cop[1]
        c_3 = self.c_cop[2]
        c_4 = self.c_cop[3]

        # Limit minimum src_side_eft used in correlation to -10
        _src_side_eft = max(src_side_eft, -10)
        return c_1 + c_2 * load_side_exft + c_3 * load_side_exft ** 2 + c_4 * _src_side_eft

    def x7_capacity(self, src_side_eft, load_side_exft):
        """
        Gives capacity in W of the "X7" heat pump;
        data provided by Martin Forszn for an actual Swedish
        heat pump, but anonymized, so to speak.

        The capacity is for the vapor compression cycle only

        Input variables:

        src_side_eft: Source-side Entering Fluid Temperature(C)
           i.e. coming from ground heat exchanger
           will include some antifreeze
           Range +5 > src_side_eft > -5

        load_side_exft: Load-side Exiting Fluid Temperature(C)
            i.e. hot water going either to heat domestic hot water
            via double shell tank
            or to panel radiators

        Coefficients are derived using GLSQ
           Range +60 > load_side_exft > +35

        JDS 20130605

        :param src_side_eft: Source-side Entering Fluid Temperature(C)
        :param load_side_exft: Load-side Exiting Fluid Temperature(C)
        :return: capacity (W)
        """

        c_1 = self.c_capacity[0]
        c_2 = self.c_capacity[1]
        c_3 = self.c_capacity[2]
        c_4 = self.c_capacity[3]

        # Limit minimum src_side_eft used in correlation to -10
        _src_side_eft = max(src_side_eft, -10)
        return c_1 + c_2 * load_side_exft + c_3 * load_side_exft ** 2 + c_4 * _src_side_eft

    def calc_wtr_htg(self, time, dt, src_side_eft):
        capacity = self.x7_capacity(src_side_eft, self.wtr_htg_set_point) * sec_to_hr(dt)
        imm_htr_capacity = self.imm_htr_capacity
        cop = self.x7_cop(src_side_eft, self.wtr_htg_set_point)
        load = self.wtr_htg_loads.get_value(time)

        imm_elec = 0  # electricity consumption of immersion heater (kW)
        unmet = 0  # unmet load

        if capacity >= load:
            # water heating load can be met with heat pump
            elec = load / cop
            rtf = load / capacity
            heat_extraction = load - elec
        elif (capacity + imm_htr_capacity) >= load:
            # water heating load can be met with heat pump and water heater
            rtf = 1
            elec = capacity / cop
            imm_elec = load - capacity
            heat_extraction = capacity - elec
        else:
            # water heating load cannot be met
            rtf = 1
            elec = capacity / cop
            imm_elec = imm_htr_capacity
            heat_extraction = capacity - elec
            unmet = load - capacity - imm_htr_capacity

        self.wtr_htg_elec = elec
        self.wtr_htg_rtf = rtf
        self.wtr_htg_imm_elec = imm_elec
        self.wtr_htg_unmet = unmet
        self.heat_extraction = heat_extraction

    def set_htg_exft(self, time):
        # outdoor air temperature
        odt = self.oda_temps.get_value(time)

        # implement control curve
        if odt < self.odt_at_max_htg_set_point:
            # heating set point to maximum value
            htg_exft = self.max_htg_set_point
        elif odt > self.odt_at_min_htg_set_point:
            # heating set point to minimum value
            htg_exft = self.min_htg_set_point
        else:
            # interpolate between max/min
            htg_exft = lin_interp(odt,
                                  self.odt_at_max_htg_set_point,
                                  self.odt_at_min_htg_set_point,
                                  self.max_htg_set_point,
                                  self.min_htg_set_point)
        return htg_exft

    def calc_htg(self, time, dt, src_side_eft):

        htg_exft = self.set_htg_exft(time)

        available_rtf = 1 - self.wtr_htg_rtf
        capacity = (self.x7_capacity(src_side_eft, self.wtr_htg_set_point) * sec_to_hr(dt)) * available_rtf
        imm_htr_capacity = self.imm_htr_capacity - self.wtr_htg_imm_elec
        cop = self.x7_cop(src_side_eft, htg_exft)
        load = self.htg_loads.get_value(time)

        imm_elec = 0  # electricity consumption of immersion heater (kW)
        unmet = 0  # unmet load

        if capacity >= load:
            # water heating load can be met with heat pump
            elec = load / cop
            rtf = load / capacity * available_rtf
            heat_extraction = load - elec
        elif (capacity + imm_htr_capacity) >= load:
            # water heating load can be met with heat pump and water heater
            rtf = 1
            elec = capacity / cop
            imm_elec = load - capacity * available_rtf
            heat_extraction = capacity - elec
        else:
            # water heating load cannot be met
            rtf = 1
            elec = capacity / cop
            imm_elec = imm_htr_capacity
            heat_extraction = capacity - elec
            unmet = load - capacity - imm_htr_capacity

        self.htg_elec = elec
        self.htg_rtf = rtf
        self.htg_imm_elec = imm_elec
        self.htg_unmet = unmet
        self.heat_extraction += heat_extraction

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        time = inputs.time
        dt = inputs.time_step
        inlet_temp = inputs.temperature

        # model prioritizes water heating above space heating
        # so these must be done in order
        self.calc_wtr_htg(time, dt, inlet_temp)
        self.calc_htg(time, dt, inlet_temp)

        return inputs

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature}
