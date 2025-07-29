"""
Drift of eDNA particles in the ocean
=======================================
"""
from datetime import timedelta, datetime
from opendrift.models.pelagicegg import eDNADrift
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers import reader_shape
import numpy as np
import os
from shapely.geometry import Point, shape
import fiona

# Paths to environmental data
enviro_path = "../data/enviro/adriatic2024/"
reader_wp1 = reader_netCDF_CF_generic.Reader(enviro_path + "cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_1716248882171.nc")
reader_wp2 = reader_netCDF_CF_generic.Reader(enviro_path + "cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m_1716248968702.nc")
print(reader_wp1)
print(reader_wp2)

# Path to shapefile for coastlines
coastline_shapefile = '../data/shp/Europe_coastline_shapefile/Europe_coastline.shp'

# Function to check if a point is in the sea
def is_point_in_sea(lon, lat, coastline_shapes):
    point = Point(lon, lat)
    for coastline_shape in coastline_shapes:
        if coastline_shape.contains(point):
            return False
    return True

# Load the coastline shapes
with fiona.open(coastline_shapefile, 'r') as shp:
    coastline_shapes = [shape(feature['geometry']) for feature in shp]

# Define the grid resolution and coordinate limits
min_lon = 12.802152
max_lon = 19.2555555
min_lat = 40.1747017584095
max_lat = 45.865043973178935
resolution = 0.25

# Create a grid of points
lon_points = np.arange(min_lon, max_lon, resolution)
lat_points = np.arange(min_lat, max_lat, resolution)

# Ensure the output directory exists
output_path = "../data/output/adriatic2024/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Pre-filter points based on land/ocean
filtered_points = []
for lon in lon_points:
    for lat in lat_points:
        if is_point_in_sea(lon, lat, coastline_shapes):
            filtered_points.append((lon, lat))

# Run the model for each filtered point
time_start = datetime(2024, 5, 25)
for lon, lat in filtered_points:
    try:
        # Re-initialize the model for each run
        o = eDNADrift(loglevel=20)  # 0 for debug output
        
        # Add readers to the model
        o.add_reader(reader_wp1)
        o.add_reader(reader_wp2)
        o.add_reader(reader_shape.Reader.from_shpfiles(coastline_shapefile))
        
        # Enable auto landmask
        o.set_config('general:use_auto_landmask', True)

        # Adjust configuration settings
        o.set_config('drift:vertical_mixing', True)
        o.set_config('vertical_mixing:diffusivitymodel', 'environment')  # Use eddy diffusivity from ocean model
        o.set_config('vertical_mixing:timestep', 60.)  # Seconds
        o.set_config('drift:current_uncertainty', 0.15)
        o.set_config('drift:wind_uncertainty', 0.2)
        o.set_config('processes:degradation', True)
        
        # Seed particles
        o.seed_elements(lon=lon, lat=lat, z=0, radius=10, number=1000,
                        time=time_start, terminal_velocity=0)
        
        # Run the model and save the output
        output_file = f"{output_path}adriatic_{lon}_{lat}.nc"
        o.run(duration=timedelta(hours=48), time_step=900, time_step_output=3600, 
              outfile=output_file)
    except ValueError as e:
        print(f"Skipping point ({lon}, {lat}) due to error: {e}")
        continue
