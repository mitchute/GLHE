from typing import Union

from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


def make_borehole(inputs, ip, op) -> Union[SingleUTubeGroutedBorehole]:
    bh_name = inputs['name']
    comp_inputs = ip.get_definition_object('borehole', bh_name)
    def_inputs = ip.get_definition_object('borehole-definitions', comp_inputs['borehole-def-name'])
    bh_type = def_inputs['borehole-type']

    if bh_type == 'single-grouted':
        return SingleUTubeGroutedBorehole(inputs, ip, op)
    else:
        raise KeyError("Borehole: '{}', Name: '{}' is not valid.".format(bh_type, bh_name))
