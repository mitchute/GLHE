class TimeStepSimulationResponse(object):

    def __init__(self, outlet_temperature=0, heat_rate=0):
        self.outlet_temperature = outlet_temperature
        self.heat_rate = heat_rate
