class ReportTypes(object):
    """
    All report variables, grouped.
    """

    # heat transfer
    HeatRate = 'Heat Rate [W]'
    HeatRateBH = 'BH Heat Rate [W]'

    # flow
    FlowRate = 'Flow Rate [kg/s]'
    VolFlowRate = 'Vol. Flow Rate [m^3/s]'

    # temperatures
    InletTemp = 'Inlet Temp. [C]'
    OutletTemp = 'Outlet Temp. [C]'
    InletTemp_Leg1 = 'Inlet Temp. Leg 1 [C]'
    InletTemp_Leg2 = 'Inlet Temp. Leg 2 [C]'
    OutletTemp_Leg1 = 'Outlet Temp. Leg 1 [C]'
    OutletTemp_Leg2 = 'Outlet Temp. Leg 2 [C]'
    BHWallTemp = 'Borehole Wall Temp. [C]'

    # resistances
    BHResist = 'BH Resist. [m-K/W]'
    BHEffResist = 'BH Eff. Resist. [m-K/W]'
    PipeResist = 'Pipe Resist. [m-K/W]'

    # heat pump
    RTF = 'Runtime Fraction [-]'
    HtgRTF = 'Runtime Fraction for Heating [-]'
    WtrHtgRTF = 'Runtime Fraction for Water Heating [-]'
    HtgElect = 'Electrical Usage for Heating [W]'
    WtrHtgElect = 'Electrical Usage for Water Heating [W]'
    HtgImmElect = 'Electrical Usage for Immersion Heater for Heating [W]'
    WtrHtgImmElect = 'Electrical Usage for Immersion Heater fow Water Heating [W]'
    HeatRateSrc = 'Source-side Heat Rate [W]'
    HeatRateLoad = 'Load-side Heat Rate [W]'
    HpElect = 'Total Electrical Usage for Heating and Water Heating [W]'
    ImmElect = 'Total Immersion Heater Usage for Heating and Water Heating [W]'
    HtgLoad = 'Heating Load [W]'
    WtrHtgLoad = 'Water Heating Load [W]'

    # non-dimensional numbers
    ReynoldsNo = 'Reynolds No [-]'
