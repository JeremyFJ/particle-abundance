# This file is part of OpenDrift.
#
# OpenDrift is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2
#
# OpenDrift is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenDrift.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright 2020, Knut-Frode Dagestad, MET Norway

"""
SedimentDrift is an OpenDrift module for drift and settling of sediments.
Based on work by Simon Weppe, MetOcean Solutions Ltd.
"""

import numpy as np
from opendrift.models.oceandrift import OceanDrift
from opendrift.models.oceandrift import Lagrangian3DArray

class SedimentElement(Lagrangian3DArray):
    variables = Lagrangian3DArray.add_variables([
        ('settled', {'dtype': np.int16,  # 0 is active, 1 is settled
                     'units': '1',
                     'default': 0}),
        ('terminal_velocity', {'dtype': np.float32,
                               'units': 'm/s',
                               'default': -0.001})  # 1 mm/s negative buoyancy
        ])


class SedimentDrift(OceanDrift):
    """Model for sediment drift, under development
    """

    ElementType = SedimentElement

    required_variables = {
        'x_sea_water_velocity': {'fallback': 0},
        'y_sea_water_velocity': {'fallback': 0},
        'upward_sea_water_velocity': {'fallback': 0},
        'x_wind': {'fallback': 0},
        'y_wind': {'fallback': 0},
        'sea_surface_wave_stokes_drift_x_velocity': {'fallback': 0},
        'sea_surface_wave_stokes_drift_y_velocity': {'fallback': 0},
        'sea_surface_wave_period_at_variance_spectral_density_maximum': {'fallback': 0},
        'sea_surface_wave_mean_period_from_variance_spectral_density_second_frequency_moment': {'fallback': 0},
        'land_binary_mask': {'fallback': None},
        'ocean_vertical_diffusivity': {'fallback': 0.02},
        'sea_floor_depth_below_sea_level': {'fallback': 0},
        }

    def __init__(self, *args, **kwargs):
        """ Constructor of SedimentDrift module
        """

        super(SedimentDrift, self).__init__(*args, **kwargs)

        # By default, sediments do not strand towards coastline
        # TODO: A more sophisticated stranding algorithm is needed
        self._set_config_default('general:coastline_action', 'previous')

        # Vertical mixing is enabled as default
        self._set_config_default('drift:vertical_mixing', True)

    def update(self):
        """Update positions and properties of sediment particles.
        """

        # Advecting here all elements, but want to soon add 
        # possibility of not moving settled elements, until
        # they are resuspended. May then need to send a boolean
        # array to advection methods below
        self.advect_ocean_current()

        self.vertical_advection()

        self.advect_wind()  # Wind shear in upper 10cm of ocean

        self.stokes_drift()

        self.vertical_mixing()  # Including buoyancy and settling

        self.resuspension()

    def bottom_interaction(self, seafloor_depth):
        """Sub method of vertical_mixing, determines settling"""
        # Elements at or below seafloor are settled, by setting
        # self.elements.moving to 0.
        # These elements will not move until eventual later resuspension.
        settling = np.logical_and(self.elements.z <= seafloor_depth, self.elements.moving==1)
        if np.sum(settling) > 0:
            self.logger.debug('Settling %s elements at seafloor' % np.sum(settling))
            self.elements.moving[settling] = 0

    def resuspension(self):
        """Resuspending elements if current speed > .5 m/s"""
        resuspending = np.logical_and(self.current_speed()>.5, self.elements.moving==0)
        if np.sum(resuspending) > 0:
            # Allow moving again
            self.elements.moving[resuspending] = 1
            # Suspend 1 cm above seafloor
            self.elements.z[resuspending] = self.elements.z[resuspending] + .01


######################################
######################################
######################################

import datetime
import numpy as np
import logging;

logger = logging.getLogger(__name__)
from opendrift.models.oceandrift import Lagrangian3DArray, OceanDrift

class eDNAElement(Lagrangian3DArray):
    """
    Extending Lagrangian3DArray with specific properties for larval and juvenile stages of fish
    """

    variables = Lagrangian3DArray.add_variables([
        ('diameter', {'dtype': np.float32,
                      'units': 'm',
                      'default': 0.0014}),  # for NEA Cod
        ('neutral_buoyancy_salinity', {'dtype': np.float32,
                                       'units': 'PSU',
                                       'default': 31.25}),  # for NEA Cod
        ('stage_fraction', {'dtype': np.float32,  # to track percentage of development time completed
                            'units': '',
                            'default': 0.}),
        ('hatched', {'dtype': np.int64,  # 0 for eggs, 1 for larvae
                     'units': '',
                     'default': 0}),
        ('length', {'dtype': np.float32,
                    'units': 'mm',
                    'default': 0}),
        ('weight', {'dtype': np.float32,
                    'units': 'mg',
                    'default': 0.08}),
        ('survival', {'dtype': np.float32,  # Not yet used
                      'units': '',
                      'default': 1.})])


class eDNADrift(OceanDrift):
    """Buoyant particle trajectory model based on the OpenDrift framework.

        Developed at MET Norway

        Generic module for particles that are subject to vertical turbulent
        mixing with the possibility for positive or negative buoyancy

        Particles could be e.g. oil droplets, plankton, or sediments

    """

    ElementType = eDNAElement

    required_variables = {
        'x_sea_water_velocity': {'fallback': 0},
        'y_sea_water_velocity': {'fallback': 0},
        'sea_surface_wave_significant_height': {'fallback': 0},
        'x_wind': {'fallback': 0},
        'y_wind': {'fallback': 0},
        'land_binary_mask': {'fallback': None},
        'sea_floor_depth_below_sea_level': {'fallback': 100},
        'ocean_vertical_diffusivity': {'fallback': 0.01, 'profiles': True},
        'sea_water_temperature': {'fallback': 10, 'profiles': True},
        'sea_water_salinity': {'fallback': 34, 'profiles': True}
    }

    required_profiles_z_range = [0, -500]  # The depth range (in m) which profiles should cover

    def __init__(self, *args, **kwargs):
        # Calling general constructor of parent class
        super(eDNADrift, self).__init__(*args, **kwargs)

        self._set_config_default('general:coastline_action', 'previous')
        self._set_config_default('drift:vertical_mixing', True)

def fish_growth(self, weight, temperature):
    # Weight in milligrams, temperature in celcius
    # Daily growth rate in percent according to
    # Folkvord, A. 2005. "Comparison of Size-at-Age of Larval Atlantic Cod (Gadus Morhua)
    # from Different Populations Based on Size- and Temperature-Dependent Growth
    # Models." Canadian Journal of Fisheries and Aquatic Sciences.
    # Journal Canadien Des Sciences Halieutiques # et Aquatiques 62(5): 1037-52.
    GR = 1.08 + 1.79 * temperature - 0.074 * temperature * np.log(weight) \
         - 0.0965 * temperature * np.log(weight) ** 2 \
         + 0.0112 * temperature * np.log(weight) ** 3

    # Growth rate(g) converted to milligram weight (gr_mg) per timestep:
    g = (np.log(GR / 100. + 1)) * self.time_step.total_seconds() / 86400
    return weight * (np.exp(g) - 1.)


def update_eDNA(self):
    # Hatching of eggs
    active = np.where(self.elements.degraded == 0)[0]
    if len(active) > 0:
        eDNA_duration = np.exp(3.65 - 0.145 * self.environment.sea_water_temperature[
            eggs])  # Total egg development time (days) according to ambient temperature (Ellertsen et al. 1988)
        days_in_timestep = self.time_step.total_seconds() / (
                    60 * 60 * 24)  # The fraction of a day completed in one time step
        amb_fraction = days_in_timestep / amb_duration  # Fraction of development time completed during present time step
        self.elements.stage_fraction[
            eggs] += amb_fraction  # Add fraction completed during present timestep to cumulative fraction completed
        hatching = np.where(self.elements.stage_fraction[eggs] >= 1)[0]
        if len(hatching) > 0:
            logger.debug('Hatching %s eggs' % len(hatching))
            self.elements.hatched[eggs[hatching]] = 1  # Eggs with total development time completed are hatched (1)

    larvae = np.where(self.elements.hatched == 1)[0]
    if len(larvae) == 0:
        logger.debug('%s eggs, with maximum stage_fraction of %s (1 gives hatching)'
                     % (len(eggs), self.elements.stage_fraction[eggs].max()))
        return


def update(self):
    self.update_fish_larvae()
    self.advect_ocean_current()
    self.update_terminal_velocity()
    self.vertical_mixing()
    self.larvae_vertical_migration()