"""
Drift of eDNA particles in the ocean
=======================================
"""
import os
# os.chdir("../particle-abundance/scripts")
from datetime import timedelta, datetime
# from pelagicegg import eDNADrift
from opendrift.models.pelagicegg import eDNADrift
from opendrift.readers import reader_netCDF_CF_generic
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from opendrift.readers import reader_shape
import numpy as np
import pandas as pd

o = eDNADrift(loglevel=20)  # 0 for debug output

enviro_path = "../data/enviro/westpalm2023/"
reader_wp1 = reader_netCDF_CF_generic.Reader(enviro_path+"cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_1710127071877.nc")
reader_wp2 = reader_netCDF_CF_generic.Reader(enviro_path+"cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1710127404151.nc")
print(reader_wp1)
print(reader_wp2)
o.add_reader(reader_wp1)
o.add_reader(reader_wp2)
reader_coast = reader_shape.Reader.from_shpfiles('../data/shp/data_EPSG_4326/North_America.shp')
o.add_reader(reader_coast)
o.set_config('general:use_auto_landmask', False)

# Adjusting some configuration
o.set_config('drift:vertical_mixing', True)
#o.set_config('deactivate_elements', True)
o.set_config('vertical_mixing:diffusivitymodel', 'environment') # use eddy diffusivity from ocean model
# Vertical mixing requires fast time step
o.set_config('vertical_mixing:timestep', 60.) # seconds
#Set max age of particles
#o.set_config('drift:max_age_seconds', 432000) #5days
#o.set_config('deactivate_elements', False)
# Adding some diffusion
o.set_config('drift:current_uncertainty', 0.15)
o.set_config('drift:wind_uncertainty', 0.2)
o.set_config('processes:degradation', True)

# Creating sequences for longitude and latitude
lon_seq = np.arange(-180, 180.5, 0.5)  # .5 added to the stop value to include endpoint
lat_seq = np.arange(-90, 90.5, 0.5)  # Same reason as above

# Creating the grid of points
lon, lat = np.meshgrid(lon_seq, lat_seq)
grid_points = pd.DataFrame({'lon': lon.ravel(), 'lat': lat.ravel()})

# Defining the latitude and longitude limits
lat_limits = [24.761542690554872, 28.771231144268103]
lon_limits = [-80.74254581767671, -76.47928022855079]

# Filtering the points within the specified limits
filtered_points = grid_points[
    (grid_points['lat'] >= lat_limits[0]) & (grid_points['lat'] <= lat_limits[1]) &
    (grid_points['lon'] >= lon_limits[0]) & (grid_points['lon'] <= lon_limits[1])
]
len(filtered_points)

time_start = datetime(2023, 3, 25)
o.seed_elements(lon=-77.5, lat=26.5, z=0, radius=10, number=5000,
             time=time_start, terminal_velocity=0)
o.run(duration=timedelta(hours=48), time_step=900, time_step_output=3600, 
            outfile="../data/output/wpMarch2023.nc")

# o.plot(fast=False, buffer=0.2)
o.plot(fast=False, buffer=0.2,filename="../data/output/wpMarch2023.jpg", )
# # Animate sediment particles colored by their depth
# o.animation(color='z', fast=True, buffer=0.02) #buffer gives zoom of plot

