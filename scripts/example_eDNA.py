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
reader_BIOT = reader_netCDF_CF_generic.Reader('../BIOT_data/Peros_atoll/Velocity/Interpolated/merged.nc')
print(reader_BIOT)
o.add_reader(reader_BIOT)
reader_atolls = reader_shape.Reader.from_shpfiles('../BIOT_data/Shapefiles/Chagos_atolls.shp')
o.add_reader(reader_atolls)
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
time = reader_BIOT.start_time

#o.seed_elements(71.75,-5.37, z=-15,radius= 10, number=1000,
 #            time=datetime(2021, 5, 21, 12, 00, 0), terminal_velocity=0) #settling rate of 25m/day
#o.run(steps=(96*6), time_step=900) #, outfile="../Results/PB/Grid/020421/PB_71_70E_5_22S.nc")
#o.seed_elements(71.7,-5.27, z=-15,radius= 10, number=1000,
 #            time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_70E_5_27S.nc")
#o.seed_elements(71.7,-5.32, z=-15,radius= 10, number=1000,
 #           time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)#
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_70E_5_32S.nc")
#o.seed_elements(71.7,-5.37, z=-15,radius= 10, number=1000,
#             time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_70E_5_37S.nc")
#o.seed_elements(71.7,-5.42, z=-15,radius= 10, number=1000,
 #          time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_70E_5_42S.nc")
#o.seed_elements(71.7,-5.47, z=-15,radius= 10, number=1000,
 #            time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_70E_5_47S.nc")
#o.seed_elements(71.75,-5.22, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_75E_5_22S.nc")
#o.seed_elements(71.75,-5.27, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_75E_5_27S.nc")
#o.seed_elements(71.75,-5.32, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_75E_5_32S.nc")
#o.seed_elements(71.75,-5.37, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_75E_5_37S.nc")
#o.seed_elements(71.75,-5.42, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_75E_5_42S.nc")
#o.seed_elements(71.75,-5.47, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_75E_5_47S.nc")
#o.seed_elements(71.8,-5.22, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_80E_5_22S.nc")
#o.seed_elements(71.8,-5.27, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_80E_5_27S.nc")
#o.seed_elements(71.8,-5.32, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_80E_5_32S.nc")
#o.seed_elements(71.8,-5.37, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_80E_5_37S.nc")
#o.seed_elements(71.8,-5.42, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_80E_5_42S.nc")
#o.seed_elements(71.8,-5.47, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_80E_5_47S.nc")
#o.seed_elements(71.85,-5.22, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_85E_5_22S.nc")
#o.seed_elements(71.85,-5.27, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_85E_5_27S.nc")
#o.seed_elements(71.85,-5.32, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_85E_5_32S.nc")
#o.seed_elements(71.85,-5.37, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_85E_5_37S.nc")
#o.seed_elements(71.85,-5.42, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_85E_5_42S.nc")
#o.seed_elements(71.85,-5.47, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900)#, outfile="../Results/PB/Grid/020421/PB_71_85E_5_47S.nc")
#o.seed_elements(71.9,-5.22, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_90E_5_22S_10000.nc")
#o.seed_elements(71.9,-5.27, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_90E_5_27S.nc")
#o.seed_elements(71.9,-5.32, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_90E_5_32S.nc")
#o.seed_elements(71.9,-5.37, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_90E_5_37S.nc")
#o.seed_elements(71.9,-5.42, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_90E_5_42S.nc")
#o.seed_elements(71.9,-5.47, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_90E_5_47S.nc")
#o.seed_elements(71.95,-5.22, z=-15,radius= 10, number=1000,
 #              time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_95E_5_22S.nc")
#o.seed_elements(71.95,-5.27, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_95E_5_27S.nc")
#o.seed_elements(71.95,-5.32, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_95E_5_32S.nc")
#o.seed_elements(71.95,-5.37, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_95E_5_37S.nc")
#o.seed_elements(71.95,-5.42, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_95E_5_42S.nc")
#o.seed_elements(71.95,-5.47, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_95E_5_47S.nc")
#o.seed_elements(72.0,-5.22, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_72_00E_5_22S.nc")
#o.seed_elements(72.0,-5.27, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_72_00E_5_27S.nc")
#o.seed_elements(72.0,-5.32, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_72_00E_5_32S.nc")
#o.seed_elements(72.0,-5.37, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_72_00E_5_37S.nc")
#o.seed_elements(72.0,-5.42, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_72_00E_5_42S.nc")
#o.seed_elements(72.0,-5.47, z=-15,radius= 10, number=1000,
 #               time=datetime(2021, 4, 2, 00, 00, 0), terminal_velocity=0)
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_72_00E_5_47S.nc")

## 1 mm/s settling speed for 10um particle from Sediment and Contaminant Transport in Surface Waters By Wilbert Lick
#%%

o.seed_elements(71.85,-5.46, z=-15,radius= 10, number=1000,
                time=datetime(2021, 4, 30, 00, 00, 0), terminal_velocity=0)
o.run(steps=(96*6), time_step=900)#, outfile="../Results/Test/PB_71_90E_5_22S_100000.nc")


#time_step in seconds -> 1800 seconds is half an hour, 48 half hours in 1 day, 96 quarter hours in a day
#o.run(steps=(96*6), time_step=900, outfile="../Results/PB/Grid/020421/PB_71_70E_5_37S.nc")
#o.run(time_step=600, time_step_output=1800, duration=timedelta(hours=72))

#%%
print(o)

# Plotting the depth vs time
#o.plot_property('z')
o.plot_property('lat')
o.plot_property('lon')
#print(o.num_elements_active())


o.plot(fast=False, buffer=0.2)
#%%
# Animate sediment particles colored by their depth
#o.animation(color='z', fast=False, buffer=0.2) #buffer gives zoom of plot
o.animation(color='moving', fast=False, buffer=.02)

#%%
# .. image:: /gallery/animations/example_sediments_0.gif
