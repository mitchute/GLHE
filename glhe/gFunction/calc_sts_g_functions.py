from math import log, sqrt

import numpy as np

from glhe.gFunction.radial_sts_cell import RadialCell
from glhe.globals.constants import PI
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.functions import tdma
from glhe.gFunction.radial_cell_types import RadialCellType

class STSGFunctions(object):
    """
     X. Xu and Jeffrey D. Spitler. 2006. 'Modeling of Vertical Ground Loop Heat Exchangers
     with Variable Convective Resistance and Thermal Mass of the Fluid.' in Proceedings of
     the 10th International Conference on Thermal Energy Storage-EcoStock. Pomona, NJ, May 31-June 2.
    """

    def __init__(self, inputs):

        # cell numbers
        self.NUM_PIPE_CELLS = 4
        self.NUM_CONV_CELLS = 1
        self.NUM_FLUID_CELLS = 3
        self.NUM_GROUT_CELLS = 27
        self.NUM_SOIL_CELLS = 500

        # setup pipe, convection, and fluid geometries
        pipe_thickness = inputs['pipe thickness']
        self.pcf_cell_thickness = pipe_thickness / self.NUM_PIPE_CELLS
        self.pipe_inner_radius = sqrt(2) * inputs['pipe outer radius']
        self.pipe_outer_radius = self.pipe_inner_radius - pipe_thickness
        self.conv_radius = self.pipe_inner_radius - self.NUM_CONV_CELLS * self.pcf_cell_thickness

        # accounts for half thickness boundary cell
        self.fluid_radius = self.conv_radius - (self.NUM_FLUID_CELLS - 0.5) * self.pcf_cell_thickness

        # setup grout layer geometry
        self.grout_radius = inputs['borehole radius']
        self.grout_cell_thickness = (self.grout_radius - self.pipe_outer_radius) / self.NUM_GROUT_CELLS

        # setup soil layer geometry
        self.soil_radius = 10
        self.soil_cell_thickness = (self.soil_radius - self.grout_radius) / self.NUM_SOIL_CELLS

        # other
        self.soil_temperature = inputs['soil temperature']
        bh_resist = inputs['borehole resistance']
        pipe_conv_resist = inputs['pipe-convection resistance']
        self.bh_equiv_resist_tube_grout = bh_resist - pipe_conv_resist / 2.0
        self.bh_equiv_resit_conv = bh_resist - self.bh_equiv_resist_tube_grout

        self.cells = []

        # initialize fluid cells
        for i in range(self.NUM_FLUID_CELLS):

            inner_radius = self.bh_radius + i * self.soil_cell_thickness

            cell_inputs = {'type': RadialCellType.FLUID,
                           'inner radius': inner_radius,
                           'thickness': self.pcf_cell_thickness,
                           'conductivity': inputs['soil conductivity'],
                           'density': inputs['soil density'],
                           'specific heat': inputs['soil specific heat'],
                           'initial temperature': inputs['soil temperature']}

            cells.append(RadialCell(cell_inputs))


    def calc_sts_g_functions(self):

        a = np.zeros(self.NUM_SOIL_CELLS)
        b = np.zeros(self.NUM_SOIL_CELLS)
        c = np.zeros(self.NUM_SOIL_CELLS)
        d = np.zeros(self.NUM_SOIL_CELLS)

        heat_flux = 40

        time = 0
        time_step = 60
        final_time = SEC_IN_HOUR * 5

        while True:

            # TDMA setup
            for idx, this_cell in enumerate(self.cells):

                if idx == 0:

                    east_cell = self.cells[idx + 1]

                    FE1 = log(this_cell.radius_outer / this_cell.radius_center) / (2 * PI * this_cell.conductivity)
                    FE2 = log(east_cell.radius_center / east_cell.radius_inner) / (2 * PI * east_cell.conductivity)
                    AE = 1 / (FE1 + FE2)

                    AD = this_cell.vol_heat_capacity * this_cell.volume / time_step

                    a[idx] = 0
                    b[idx] = -AE / AD - 1
                    c[idx] = AE / AD
                    d[idx] = -this_cell.prev_temperature - heat_flux / AD

                elif idx == self.NUM_SOIL_CELLS - 1:

                    a[idx] = 0
                    b[idx] = 1
                    c[idx] = 0
                    d[idx] = this_cell.prev_temperature

                else:

                    west_cell = self.cells[idx - 1]
                    east_cell = self.cells[idx + 1]

                    FE1 = log(this_cell.radius_outer / this_cell.radius_center) / (2 * PI * this_cell.conductivity)
                    FE2 = log(east_cell.radius_center / east_cell.radius_inner) / (2 * PI * east_cell.conductivity)
                    AE = 1 / (FE1 + FE2)

                    FW1 = log(west_cell.radius_outer / west_cell.radius_center) / (2 * PI * west_cell.conductivity)
                    FW2 = log(this_cell.radius_center / this_cell.radius_inner) / (2 * PI * this_cell.conductivity)
                    AW = -1 / (FW1 + FW2)

                    AD = this_cell.vol_heat_capacity * this_cell.volume / time_step

                    a[idx] = -AW / AD
                    b[idx] = AW / AD - AE / AD - 1
                    c[idx] = AE / AD
                    d[idx] = -this_cell.prev_temperature

            temps = tdma(a, b, c, d)

            for idx, this_cell in enumerate(self.cells):
                this_cell.prev_temperature = this_cell.temperature
                this_cell.temperature = temps[idx]

            time += time_step
            if time > final_time:
                break

        pass
