"""
Drift of eDNA particles in the ocean
=======================================
"""
from datetime import timedelta, datetime
from opendrift.models.pelagicegg import eDNADrift
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers import reader_shape

# Paths to environmental data
enviro_path = "../data/enviro/adriatic2024/"
reader_wp1 = reader_netCDF_CF_generic.Reader(enviro_path + "cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_1716248882171.nc")
reader_wp2 = reader_netCDF_CF_generic.Reader(enviro_path + "cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m_1716248968702.nc")
print(reader_wp1)
print(reader_wp2)

# Path to shapefile for coastlines
coastline_shapefile = '../data/shp/Europe_coastline_shapefile/Europe_coastline.shp'

# Re-initialize the model for each run
o = eDNADrift(loglevel=20)  # 0 for debug output

# Add readers to the model
o.add_reader(reader_wp1)
o.add_reader(reader_wp2)
# o.add_reader(reader_shape.Reader.from_shpfiles(coastline_shapefile))


# Enable auto landmask
o.set_config('general:use_auto_landmask', True)

# Adjust configuration settings
o.set_config('drift:vertical_mixing', True)
o.set_config('vertical_mixing:diffusivitymodel', 'environment')  # Use eddy diffusivity from ocean model
o.set_config('vertical_mixing:timestep', 60.)  # Seconds
o.set_config('drift:current_uncertainty', 0.15)
o.set_config('drift:wind_uncertainty', 0.2)
o.set_config('processes:degradation', True)
time_start = datetime(2024, 5, 25)
output_path = "../data/output/adriatic2024/"
# Seed particles
o.seed_elements(lat=43.8, lon=13.8, z=0, radius=1, number=10000,
time=time_start, terminal_velocity=0)

# Run the model and save the output
output_file = f"{output_path}adriatic.nc"
o.run(duration=timedelta(hours=96), time_step=900, time_step_output=3600)
o.animation(color='z', fast=True, buffer=0.15, filename="../figures/adriatic2024_anim.mp4") #buffer gives zoom of plot
# outfile=output_file)
o.plot(fast=False, buffer=0.15,filename="../figures/adriatic2024_plot.jpg", )