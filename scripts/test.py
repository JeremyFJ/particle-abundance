from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.pelagicegg import PelagicEggDrift
from datetime import datetime, timedelta
import os

o = PelagicEggDrift(loglevel=20)  # Set loglevel to 0 for debug information
enviro_path = "/Users/jjeremy1/Dropbox/eDNA/particle-abundance/data/enviro/sicily2021/"
enviro_list = ["sicily2021_salinity.nc", "sicily2021_mixture.nc", 
                         "sicily2021_temp.nc", "sicily2021_velocity.nc",
                         "sicily2021_upward.nc", "sicily2021_temp.nc"]
all_enviro = [os.path.join(enviro_path, filename) for filename in enviro_list]
o.add_readers_from_list(all_enviro)
# r = reader_netCDF_CF_generic.Reader("tunis2022.nc")
# time = datetime.utcnow()
time = datetime(2021, 6, 19, 9, 16, 2, 181582) 
o.seed_elements(12.352, 35.621, z=-30, radius=2000, number=10000, density = 1000,
                time=time, diameter=0.00001, neutral_buoyancy_salinity=31)
o.set_config('drift:vertical_mixing', False)
# o.set_config('vertical_mixing:diffusivitymodel', 'windspeed_Sundby1983') # windspeed parameterization for eddy diffusivity
# o.set_config('vertical_mixing:timestep', 60) # seconds
o.set_config('environment:fallback:x_wind', 1)
o.set_config('environment:fallback:y_wind', 2)
# o.set_config('environment:fallback:ocean_mixed_layer_thickness', 0)

o.run(duration=timedelta(hours=-72), time_step=-5200, outfile="./testing.nc") # tracks backwards in time 3 days

# o.plot(fast=True)
# o.animation(fast=True, color='z')
# o.animate_vertical_distribution()