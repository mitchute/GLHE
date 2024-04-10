from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.single_u_tube_grouted_borehole import SingleUTubeGroutedBorehole


def make_borehole(inputs: dict, ip: InputProcessor, op: OutputProcessor) -> SingleUTubeGroutedBorehole:
    bh_name = inputs['name']
    if 'average-borehole' not in inputs:
        comp_inputs = ip.get_definition_object('borehole', bh_name)
        def_inputs = ip.get_definition_object('borehole-definitions', comp_inputs['borehole-def-name'])
        bh_type = def_inputs['borehole-type']
    else:
        bh_type = inputs['borehole-type']

    if bh_type == 'single-grouted':
        return SingleUTubeGroutedBorehole(inputs, ip, op)
    else:
        raise KeyError("Borehole: '{}', Name: '{}' is not valid.".format(bh_type, bh_name))  # pragma: no cover
