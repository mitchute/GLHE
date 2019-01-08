from glhe.gFunction.radial_sts_cell import RadialCell


class STSGFunctions(object):

    """
      X. Xu and Jeffrey D. Spitler. 2006. 'Modeling of Vertical Ground Loop Heat Exchangers
      with Variable Convective Resistance and Thermal Mass of the Fluid.' in Proceedings of
      the 10th International Conference on Thermal Energy Storage-EcoStock. Pomona, NJ, May 31-June 2
    """

    def __init__(self, inputs):
        self.bh_radius = inputs['borehole radius']
        self.SOIL_RADIUS = 10
        self.NUM_SOIL_CELLS = 500
        self.soil_temperature = inputs['soil temperature']
        self.soil_cell_thickness = (self.SOIL_RADIUS - self.bh_radius) / self.NUM_SOIL_CELLS
        self.cells = self.make_cells(inputs)

    def make_cells(self, inputs):
        cells = []

        for i in range(self.NUM_SOIL_CELLS):
            inner_radius = self.bh_radius + i * self.soil_cell_thickness

            cell_inputs = {'inner radius': inner_radius,
                           'thickness': self.soil_cell_thickness,
                           'conductivity': inputs['soil conductivity'],
                           'density': inputs['soil density'],
                           'specific heat': inputs['soil specific heat'],
                           'initial temperature': inputs['soil temperature']}

            cells.append(RadialCell(cell_inputs))

        return cells

    def calc_sts_g_functions(self, inputs):
        pass
