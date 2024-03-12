#!/usr/bin/env python
"""
Drift of eDNA particles in ocean
=======================================
"""

from datetime import timedelta, datetime
from opendrift.models.pelagicegg import eDNADrift
from opendrift.readers import reader_netCDF_CF_generic
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from opendrift.readers import reader_shape
import numpy as np

o = eDNADrift(loglevel=20)  # 0 for debug output

# Try different options: 'previous', 'stranding', 'none'
o.set_config('general:coastline_action', 'previous')
reader_med = reader_netCDF_CF_generic.Reader('../Med_data/Med_water_all_merge.nc')
print(reader_med)
o.add_reader(reader_med)
reader_coast = reader_shape.Reader.from_shpfiles('../Med_data/Europe_coastline_shapefile/Med_sea.shp')
o.add_reader(reader_coast)
o.set_config('general:use_auto_landmask', False)

# Adjusting some configuration
o.set_config('drift:vertical_mixing', True)
#o.set_config('deactivate_elements', True)
o.set_config('vertical_mixing:diffusivitymodel', 'environment') # use eddy diffusivity from ocean model
# %%
# Vertical mixing requires fast time step
o.set_config('vertical_mixing:timestep', 60.) # seconds
#Set max age of particles
#o.set_config('drift:max_age_seconds', 432000) #5days
#o.set_config('deactivate_elements', False)
# Adding some diffusion
o.set_config('drift:current_uncertainty', 0.1)
o.set_config('drift:wind_uncertainty', 0.2)
o.set_config('processes:degradation', True)

#%%
# set time to start_time for forecast or end_time for hindcast
time = reader_med.start_time


#o.seed_elements(12.070578, 37.9708, z=-10,radius= 10, number=1000,
 #            time=datetime(2021, 6, 12, 14, 44, 0), terminal_velocity=0)
o.seed_elements(14, 34.5, z=0,radius= 10, number=4252,
             time=datetime(2021, 6, 30, 12, 00, 0), terminal_velocity=0)
#o.seed_elements(12.1435, 37.878383, z=-30,radius= 10, number=1000,
 #            time=datetime(2021, 6, 13, 13, 30, 0), terminal_velocity=0)
#o.seed_elements(12.352, 35.621, z=-100,radius= 10, number=1000,
 #            time=datetime(2021, 6, 18, 19, 9, 0), terminal_velocity=0)
o.run(steps=(96*6), time_step=900) #, outfile="../Results/PB/Grid/020421/PB_71_70E_5_22S.nc")

#%%
print(o)

# Plotting the depth vs time
o.plot_property('z')
o.plot_property('lat')
o.plot_property('lon')
#print(o.num_elements_active())


o.plot(fast=False, buffer=0.2)
#%%
# Animate sediment particles colored by their depth
o.animation(color='z', fast=False, buffer=0.02) #buffer gives zoom of plot
#o.animation(color='moving', fast=False, buffer=.02)

#%%
# .. image:: /gallery/animations/example_sediments_0.gif