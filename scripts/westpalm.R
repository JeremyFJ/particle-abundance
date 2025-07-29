library("rnaturalearth")
library("rnaturalearthdata")
library(tidyverse)
library(dplyr)
library(ncdf4)
library(sf)
library(ggmap)
sf_use_s2(FALSE)

setwd("~/Dropbox/eDNA/particle-abundance/scripts/")
world <- ne_countries(scale = "medium", returnclass = "sf")
nc_data <- nc_open("../data/output/wpMarch2023.nc")
# Assuming nc_data is your NetCDF dataset object
lat <- ncvar_get(nc_data, "lat")  # Use the correct variable names based on your file
lon <- ncvar_get(nc_data, "lon")
z <- ncvar_get(nc_data, "z")
degraded <- ncvar_get(nc_data, "degraded")
age_seconds <- ncvar_get(nc_data, "age_seconds")

# Combine the extracted variables into a DataFrame
df <- data.frame(lat = lat, lon = lon, z = z, degraded = degraded, age_seconds = age_seconds)
