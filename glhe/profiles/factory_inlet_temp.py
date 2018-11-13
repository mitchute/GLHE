from glhe.profiles.external_inlet_temps import ExternalInletTemps


def make_inlet_temp_profile(inputs):
    path = inputs['external']['path']
    return ExternalInletTemps(path)
