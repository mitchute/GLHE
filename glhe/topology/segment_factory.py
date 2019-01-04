from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment
from glhe.topology.single_u_tube_pass_through_segment import SingleUTubePassThroughSegment


def make_segment(inputs, fluid_inst=None, grout_inst=None, soil_inst=None, final_seg=False):
    if inputs['model'] == 'single':
        if final_seg:
            return SingleUTubePassThroughSegment(inputs)
        else:
            return SingleUTubeGroutedSegment(inputs, fluid_inst=fluid_inst, grout_inst=grout_inst, soil_inst=soil_inst)
    else:
        raise ValueError("Segment type '{}' not supported".format(inputs['model']))
