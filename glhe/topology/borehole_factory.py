from glhe.globals.functions import merge_dicts
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


def make_borehole(inputs, ip, op):
    bh_def = ip.definition_mgr.get_definition('borehole', inputs['borehole-def-name'])
    if bh_def['borehole-type'] == 'single-grouted':
        return SingleUTubeGroutedBorehole(merge_dicts(bh_def, {'initial temp': inputs['initial temp']}), ip, op)
    else:
        raise NotImplementedError("Borehole type '{}' is not valid.".format(bh_def['bh-type']))
