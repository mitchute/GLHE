class BoreholeType(object):
    """
    All borehole types, alphabetically
    """
    SINGLE_U_TUBE_GROUTED = 1


class ComponentTypes(object):
    """
    All simulatable component types, alphabetically
    """
    ConstantFlow = 'ConstantFlow'
    ConstantLoad = 'ConstantLoad'
    ExternalFlow = 'ExternalFlow'
    ExternalLoad = 'ExternalLoad'
    GroundHeatExchanger = 'GroundHeatExchanger'
    GroundHeatExchangerLTS = 'GroundHeatExchangerLTS'
    GroundHeatExchangerSTS = 'GroundHeatExchangerSTS'
    ImpulseLoad = 'ImpulseLoad'
    SinusoidLoad = 'SinusoidLoad'
    SyntheticLoad = 'SyntheticLoad'