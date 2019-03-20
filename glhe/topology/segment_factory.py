from glhe.input_processor.input_processor import InputProcessor
from glhe.output_processor.output_processor import OutputProcessor
from glhe.topology.single_u_tube_grouted_segment import SingleUTubeGroutedSegment
from glhe.topology.single_u_tube_pass_through_segment import SingleUTubePassThroughSegment


def make_segment(inputs: dict, ip: InputProcessor, op: OutputProcessor, final_seg: bool = False):
    if inputs['model'] == 'single':
        if final_seg:
            return SingleUTubePassThroughSegment(inputs)
        else:
            return SingleUTubeGroutedSegment(inputs, ip, op)
    else:
        raise ValueError("Segment type '{}' not supported".format(inputs['model']))
