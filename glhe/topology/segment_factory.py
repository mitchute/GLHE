from glhe.topology.single_u_tube_segment import SingleUTubeSegment


def make_segment(inputs, fluid):
    if inputs['model'] == 'single':
        return SingleUTubeSegment(inputs, fluid)
