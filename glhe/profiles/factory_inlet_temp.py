from glhe.profiles.external_inlet_temps import ExternalInletTemps


def make_inlet_temp_profile(inputs):
    try:
        path = inputs['external']['path']
        return ExternalInletTemps(path)
    except KeyError:
        raise KeyError("Inlet temperature path not valid")
