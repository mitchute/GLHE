from math import log, sqrt

import numpy as np

from glhe.gFunction.radial_cell_types import RadialCellType
from glhe.gFunction.radial_sts_cell import RadialCell
from glhe.globals.constants import PI
from glhe.globals.constants import SEC_IN_HOUR
from glhe.globals.functions import tdma_2


class STSGFunctions(object):
    """
     X. Xu and Jeffrey D. Spitler. 2006. 'Modeling of Vertical Ground Loop Heat Exchangers
     with Variable Convective Resistance and Thermal Mass of the Fluid.' in Proceedings of
     the 10th International Conference on Thermal Energy Storage-EcoStock. Pomona, NJ, May 31-June 2.
    """

    def __init__(self, inputs):

        # cell numbers
        num_pipe_cells = 4
        num_conv_cells = 1
        num_fluid_cells = 3
        num_grout_cells = 27
        num_soil_cells = 500

        # setup pipe, convection, and fluid geometries
        pipe_outer_dia_act = inputs['pipe outer diameter']
        pipe_inner_dia_act = inputs['pipe inner diameter']
        pipe_thickness_act = (pipe_outer_dia_act - pipe_inner_dia_act) / 2
        pipe_outer_radius_act = pipe_outer_dia_act / 2
        pipe_inner_radius_act = pipe_inner_dia_act / 2

        pcf_cell_thickness = pipe_thickness_act / num_pipe_cells
        pipe_outer_radius = sqrt(2) * pipe_outer_radius_act
        pipe_inner_radius = pipe_outer_radius - pipe_thickness_act
        conv_radius = pipe_inner_radius - num_conv_cells * pcf_cell_thickness

        # accounts for half thickness boundary cell
        fluid_radius = conv_radius - (num_fluid_cells - 0.5) * pcf_cell_thickness

        # setup grout layer geometry
        grout_radius = inputs['borehole diameter'] / 2.0
        grout_cell_thickness = (grout_radius - pipe_outer_radius) / num_grout_cells

        # setup soil layer geometry
        soil_radius = 10
        soil_cell_thickness = (soil_radius - grout_radius) / num_soil_cells

        # other
        init_temp = inputs['initial temperature']
        bh_resist = inputs['borehole resistance']
        conv_resist = inputs['convection resistance']
        bh_equiv_tube_grout_resist = bh_resist - conv_resist / 2.0
        bh_equiv_conv_resist = bh_resist - bh_equiv_tube_grout_resist

        self.cells = []

        # initialize fluid cells
        for idx in range(num_fluid_cells):

            cell_type = RadialCellType.FLUID
            thickness = pcf_cell_thickness
            center_radius = fluid_radius + idx * thickness

            if idx == 0:
                inner_radius = center_radius
            else:
                inner_radius = center_radius - thickness / 2.0

            outer_radius = center_radius + thickness / 2.0

            conductivity = 200

            rho_cp_1 = 2.0 * inputs['fluid specific heat'] * inputs['fluid density']
            rho_cp_2 = (pipe_inner_radius_act ** 2) / ((conv_radius ** 2) - (fluid_radius ** 2))
            rho_cp = rho_cp_1 * rho_cp_2

            cell_inputs = {'type': cell_type,
                           'inner radius': inner_radius,
                           'center radius': center_radius,
                           'outer radius': outer_radius,
                           'thickness': thickness,
                           'conductivity': conductivity,
                           'vol heat capacity': rho_cp,
                           'initial temperature': init_temp}

            self.cells.append(RadialCell(cell_inputs))

        # initialize convection cells
        for idx in range(num_conv_cells):
            cell_type = RadialCellType.CONVECTION
            thickness = pcf_cell_thickness
            inner_radius = conv_radius + idx * thickness
            center_radius = inner_radius + thickness / 2.0
            outer_radius = inner_radius + thickness
            conductivity = log(pipe_inner_radius / conv_radius) / (2 * PI * bh_equiv_conv_resist)
            rho_cp = 1

            cell_inputs = {'type': cell_type,
                           'inner radius': inner_radius,
                           'center radius': center_radius,
                           'outer radius': outer_radius,
                           'thickness': thickness,
                           'conductivity': conductivity,
                           'vol heat capacity': rho_cp,
                           'initial temperature': init_temp}

            self.cells.append(RadialCell(cell_inputs))

        # initialize pipe cells
        for idx in range(num_pipe_cells):
            cell_type = RadialCellType.PIPE
            thickness = pcf_cell_thickness
            inner_radius = pipe_inner_radius + idx * thickness
            center_radius = inner_radius + thickness / 2.0
            outer_radius = inner_radius + thickness
            conductivity = log(grout_radius / pipe_inner_radius) / (2 * PI * bh_equiv_tube_grout_resist)
            rho_cp = inputs['pipe density'] * inputs['pipe specific heat']

            cell_inputs = {'type': cell_type,
                           'inner radius': inner_radius,
                           'center radius': center_radius,
                           'outer radius': outer_radius,
                           'thickness': thickness,
                           'conductivity': conductivity,
                           'vol heat capacity': rho_cp,
                           'initial temperature': init_temp}

            self.cells.append(RadialCell(cell_inputs))

        # initialize grout cells
        for idx in range(num_grout_cells):
            cell_type = RadialCellType.GROUT
            thickness = grout_cell_thickness
            inner_radius = pipe_outer_radius + idx * thickness
            center_radius = inner_radius + thickness / 2.0
            outer_radius = inner_radius + thickness
            conductivity = log(grout_radius / pipe_inner_radius) / (2 * PI * bh_equiv_tube_grout_resist)
            rho_cp = inputs['grout density'] * inputs['grout specific heat']

            cell_inputs = {'type': cell_type,
                           'inner radius': inner_radius,
                           'center radius': center_radius,
                           'outer radius': outer_radius,
                           'thickness': thickness,
                           'conductivity': conductivity,
                           'vol heat capacity': rho_cp,
                           'initial temperature': init_temp}

            self.cells.append(RadialCell(cell_inputs))

        # initialize soil cells
        for idx in range(num_soil_cells):
            cell_type = RadialCellType.SOIL
            thickness = soil_cell_thickness
            inner_radius = grout_radius + idx * thickness
            center_radius = inner_radius + thickness / 2.0
            outer_radius = inner_radius + thickness
            conductivity = inputs['soil conductivity']
            rho_cp = inputs['soil density'] * inputs['soil specific heat']

            cell_inputs = {'type': cell_type,
                           'inner radius': inner_radius,
                           'center radius': center_radius,
                           'outer radius': outer_radius,
                           'thickness': thickness,
                           'conductivity': conductivity,
                           'vol heat capacity': rho_cp,
                           'initial temperature': init_temp}

            self.cells.append(RadialCell(cell_inputs))

    def calc_sts_g_functions(self):

        a = np.zeros(len(self.cells))
        b = np.zeros(len(self.cells))
        c = np.zeros(len(self.cells))
        d = np.zeros(len(self.cells))

        heat_flux = 40.4

        time = 0
        time_step = 500
        final_time = SEC_IN_HOUR * 5

        while True:

            num_cells = len(self.cells)

            # TDMA setup
            for idx, this_cell in enumerate(self.cells):

                if idx == 0:

                    east_cell = self.cells[idx + 1]

                    FE1 = log(this_cell.outer_radius / this_cell.center_radius) / (2 * PI * this_cell.conductivity)
                    FE2 = log(east_cell.center_radius / east_cell.inner_radius) / (2 * PI * east_cell.conductivity)
                    AE = 1 / (FE1 + FE2)

                    AD = this_cell.rho_cp * this_cell.volume / time_step

                    a[idx] = 0
                    b[idx] = -AE / AD - 1
                    c[idx] = AE / AD
                    d[idx] = -this_cell.prev_temperature - heat_flux / AD

                elif idx == num_cells - 1:

                    a[idx] = 0
                    b[idx] = 1
                    c[idx] = 0
                    d[idx] = this_cell.prev_temperature

                else:

                    west_cell = self.cells[idx - 1]
                    east_cell = self.cells[idx + 1]

                    FE1 = log(this_cell.outer_radius / this_cell.center_radius) / (2 * PI * this_cell.conductivity)
                    FE2 = log(east_cell.center_radius / east_cell.inner_radius) / (2 * PI * east_cell.conductivity)
                    AE = 1 / (FE1 + FE2)

                    FW1 = log(west_cell.outer_radius / west_cell.center_radius) / (2 * PI * west_cell.conductivity)
                    FW2 = log(this_cell.center_radius / this_cell.inner_radius) / (2 * PI * this_cell.conductivity)
                    AW = -1 / (FW1 + FW2)

                    AD = this_cell.rho_cp * this_cell.volume / time_step

                    a[idx] = -AW / AD
                    b[idx] = AW / AD - AE / AD - 1
                    c[idx] = AE / AD
                    d[idx] = -this_cell.prev_temperature

            temps = tdma_2(a, b, c, d)

            for idx, this_cell in enumerate(self.cells):
                this_cell.prev_temperature = this_cell.temperature
                this_cell.temperature = temps[idx]

            time += time_step
            if time > final_time:
                break

        pass
