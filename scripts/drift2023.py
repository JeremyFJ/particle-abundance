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

o = eDNADrift(loglevel=20)  # 0 for debug output

enviro_path = "../data/enviro/lamp/"
reader_wp1 = reader_netCDF_CF_generic.Reader(enviro_path+"cmems_mod_glo_phy-cur_anfc_0.083deg_PT6H-i_1710430263649.nc")
reader_wp2 = reader_netCDF_CF_generic.Reader(enviro_path+"cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i_1710430341401.nc")
print(reader_wp1)
print(reader_wp2)
o.add_reader(reader_wp1)
o.add_reader(reader_wp2)
# reader_coast = reader_shape.Reader.from_shpfiles('/Users/jjeremy1/Dropbox/eDNA/Europe_coastline/Europe_coastline_poly.shp')
# o.add_reader(reader_coast)
o.set_config('general:use_auto_landmask', True)

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
o.set_config('processes:degradation', False)


time = datetime(2023, 5, 22, 9, 16, 2, 181582) 
o.seed_elements(12.550156, 35.283502, z=0, radius=10, number=1000,
             time=time, terminal_velocity=0)
o.run(duration=timedelta(hours=-48), time_step=-900)
o.plot(fast=True, filename="../data/output/Lamp2023_2.jpg")

