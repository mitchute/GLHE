import numpy as np

from glhe.input_processor.component_types import ComponentTypes
from glhe.interface.entry import SimulationEntryPoint
from glhe.interface.response import SimulationResponse
from glhe.output_processor.report_types import ReportTypes
from glhe.profiles.external_base import ExternalBase
from glhe.properties.base_properties import PropertiesBase
from glhe.utilities.functions import kw_to_w
from glhe.utilities.functions import lin_interp


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
        self.odt = self.oda_temps.get_value(0)

        # report variables
        self.flow_rate = None
        self.inlet_temperature = None
        self.outlet_temperature = None
        self.cop = 0

        # water heating report variables
        self.wtr_htg = None  # water heating load met by heat pump (W)
        self.wtr_htg_load = None  # water heating load (W)
        self.wtr_htg_elec = None  # electricity consumption of heat pump for water heating (W)
        self.wtr_htg_rtf = None  # run time fraction of heat pump for water heating (-)
        self.wtr_htg_imm_elec = None  # electricity consumption of immersion heater for water heating (W)
        self.wtr_htg_unmet = None  # unmet water heating load (W)
        self.wtr_htg_heat_extraction = None  # heat extraction for water heating (W)

        # heating report variables
        self.htg = None  # heating load met by heat pump (W)
        self.htg_load = None  # heating load (W)
        self.htg_elec = None  # electricity consumption of heat pump for space heating (W)
        self.htg_rtf = None  # run time fraction of heat pump for space heating (-)
        self.htg_imm_elec = None  # electricity consumption of immersion heater for space heating (W)
        self.htg_unmet = None  # unmet water heating load (W)
        self.htg_heat_extraction = None  # heat extraction for space heating (W)

        # other
        self.htg_tot = None  # total heating load met by heat pump (W)
        self.imm_elec_tot = None  # total heating met by immersion heater (W)
        self.hp_rtf = None  # total heat pump runtime fraction (-)
        self.heat_extraction = None  # total heat extracted from borehole (W)

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
        return kw_to_w(c_1 + c_2 * load_side_exft + c_3 * load_side_exft ** 2 + c_4 * _src_side_eft)

    def calc_wtr_htg(self, time, src_side_eft):
        capacity = self.x7_capacity(src_side_eft, self.wtr_htg_set_point)
        imm_capacity = self.imm_htr_capacity
        cop = self.x7_cop(src_side_eft, self.wtr_htg_set_point)
        load = self.wtr_htg_loads.get_value(time)

        imm_elec = 0  # electricity consumption of immersion heater (W)
        unmet = 0  # unmet load (W)

        if load == 0:
            # no load
            rtf = 0
            htg = 0
            elec = 0
            heat_extraction = 0
        elif capacity >= load:
            # water heating load can be met with heat pump
            htg = load
            elec = load / cop
            rtf = load / capacity
            heat_extraction = load - elec
        elif (capacity + imm_capacity) >= load:
            # water heating load can be met with heat pump and water heater
            rtf = 1
            htg = capacity
            elec = capacity / cop
            imm_elec = load - capacity
            heat_extraction = capacity - elec
        else:
            # water heating load cannot be met
            rtf = 1
            htg = capacity
            elec = capacity / cop
            imm_elec = imm_capacity
            heat_extraction = capacity - elec
            unmet = load - capacity - imm_capacity

        self.wtr_htg = htg
        self.wtr_htg_load = load
        self.wtr_htg_elec = elec
        self.wtr_htg_rtf = rtf
        self.wtr_htg_imm_elec = imm_elec
        self.wtr_htg_unmet = unmet
        self.wtr_htg_heat_extraction = heat_extraction

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

    def calc_htg(self, time, src_side_eft):

        htg_exft = self.set_htg_exft(time)

        available_rtf = 1 - self.wtr_htg_rtf
        capacity = (self.x7_capacity(src_side_eft, self.wtr_htg_set_point)) * available_rtf
        imm_htr_capacity = self.imm_htr_capacity - self.wtr_htg_imm_elec
        cop = self.x7_cop(src_side_eft, htg_exft)
        self.cop = cop
        load = self.htg_loads.get_value(time)

        imm_elec = 0  # electricity consumption of immersion heater (W)
        unmet = 0  # unmet load (W)

        if load == 0:
            # no load
            rtf = 0
            htg = 0
            elec = 0
            heat_extraction = 0
        elif capacity >= load:
            # heating load can be met with heat pump
            htg = load
            elec = load / cop
            rtf = load / capacity * available_rtf
            heat_extraction = load - elec
        elif (capacity + imm_htr_capacity) >= load:
            # heating load can be met with heat pump and water heater
            rtf = available_rtf
            htg = capacity
            elec = capacity / cop
            imm_elec = load - capacity
            heat_extraction = capacity - elec
        else:
            # heating load cannot be met
            rtf = available_rtf
            htg = capacity
            elec = capacity / cop
            imm_elec = imm_htr_capacity
            heat_extraction = capacity - elec
            unmet = load - capacity - imm_htr_capacity

        self.htg = htg
        self.htg_load = load
        self.htg_elec = elec
        self.htg_rtf = rtf
        self.htg_imm_elec = imm_elec
        self.htg_unmet = unmet
        self.htg_heat_extraction = heat_extraction

    def simulate_time_step(self, inputs: SimulationResponse) -> SimulationResponse:
        time = inputs.time
        dt = inputs.time_step
        flow_rate = inputs.flow_rate
        inlet_temp = inputs.temperature

        # model prioritizes water heating above space heating
        # so these must be done in order
        self.calc_wtr_htg(time, inlet_temp)
        self.calc_htg(time, inlet_temp)

        # collect totals
        self.hp_rtf = self.wtr_htg_rtf + self.htg_rtf
        self.heat_extraction = -self.wtr_htg_heat_extraction - self.htg_heat_extraction

        cp = self.fluid.get_cp(inlet_temp)
        outlet_temp = inlet_temp + self.heat_extraction / (flow_rate * cp)
        response = SimulationResponse(time, dt, flow_rate, outlet_temp, hp_src_heat_rate=self.heat_extraction)

        # update report variables
        self.htg_tot = self.htg + self.wtr_htg
        self.imm_elec_tot = self.htg_imm_elec + self.wtr_htg_imm_elec
        self.flow_rate = flow_rate
        self.inlet_temperature = inlet_temp
        self.outlet_temperature = outlet_temp
        self.odt = self.oda_temps.get_value(time)

        return response

    def report_outputs(self) -> dict:
        return {'{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.FlowRate): self.flow_rate,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.InletTemp): self.inlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.OutletTemp): self.outlet_temperature,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRateSrc): self.heat_extraction,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HeatRateLoad): self.htg_tot,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.ImmElect): self.imm_elec_tot,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HtgLoad): self.htg_load,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.WtrHtgLoad): self.wtr_htg_load,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.RTF): self.hp_rtf,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HtgRTF): self.htg_rtf,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.WtrHtgRTF): self.wtr_htg_rtf,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HtgElect): self.htg_elec,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.WtrHtgElect): self.wtr_htg_elec,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HtgImmElect): self.htg_imm_elec,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.WtrHtgImmElect): self.wtr_htg_imm_elec,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.HtgUnmet): self.htg_unmet,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.WtrHtgUnmet): self.wtr_htg_unmet,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.ODT): self.odt,
                '{:s}:{:s}:{:s}'.format(self.Type, self.name, ReportTypes.COP): self.cop}
