### Script for reading all locations for OpenDrift particles at each timestep in simulation
#Libraries
library(maptools)
library(raster)
library(rgdal)
library(graphics)
library(maps)
library(rgeos)
library(dplyr)
library(readr)
library(geosphere)
library(ncdf4)
library(reshape2)

data(wrld_simpl)
rast <-raster()
res(rast)=0.1
###
Med  <- readOGR(dsn="/Users/nick/opendrift/Med_data/Europe_coastline_shapefile/",layer="Med_sea")
#####
######create empty plot
Sicily <-extent(10,15,33,40)
Sicily_channel <-crop(Med,Sicily)

#Set working directory for ease of data access
setwd("/Volumes/Nick_Dunn_PhD/Modelling/Med/Jan2022")
### reading in the files in the folder
EXP_files <- list.files("./", pattern = ".nc")
head(EXP_files)

for(i in 1: 90){
  file <- EXP_files[i]
  ### pulling out the latitude from the file name 
  Start_longitude <- substr(file,start=13, stop=16)
  
  ### pulling out the longitude from the file name 
  Start_latitude <- substr(file,start=18, stop=21)

  
  nc_data <- nc_open(file)
  lon <- ncvar_get(nc_data, "lon")
  lat <- ncvar_get(nc_data, "lat")
  lon[lon > 180] <- NA #this replaces the rogue values with NAs which are easier to deal with
  #Last value is where the particle was last seen
  long <- as.data.frame(lon)
  lat[lat > 180] <- NA
  lati <- as.data.frame(lat)
  longitude <- tibble::rownames_to_column(long, "Timestep_x")
  melted_longitude <- melt(longitude, value.name = "Longitude")
  melted_longitude <- tibble::rownames_to_column(melted_longitude, "VALUE")
  
  latitude <- tibble::rownames_to_column(lati, "Timestep_y")
  melted_latitude <- melt(latitude, value.name = "Latitude")
  melted_latitude <- tibble::rownames_to_column(melted_latitude, "VALUE")
  
  all_locations <- merge(melted_latitude, melted_longitude, by = "VALUE")
  all_locations <- sapply(all_locations[all_locations$VALUE ,], as.numeric)
  all_locations <- data.frame(all_locations)
  all_locations <- all_locations[order(all_locations$VALUE),]
  
  all_locations$start_lon <- as.numeric(Start_longitude)
  all_locations$start_lat <-  as.numeric(Start_latitude)
  
  all_locations <- na.omit(all_locations)
  all_locations$date <- "032022"
  
  write.csv(all_locations, 
            file = paste("/Volumes/Nick_Dunn_PhD/Modelling/Med/CSVs/January/Jan",EXP_files[i], ".csv", sep = "_"),
            row.names = FALSE)
  
}

###Read in csvs
#combine into single dataframe
df <- list.files(path="/Volumes/Nick_Dunn_PhD/Modelling/Med/CSVs/January/", full.names = TRUE) %>% 
  lapply(read_csv) %>% 
  bind_rows
df <- as.data.frame(df)
head(df)
write.csv(df, "/Volumes/Nick_Dunn_PhD/Modelling/Med/CSVs/March/March_combined.csv")

#Read in all combined csvs
setwd("/Volumes/Nick_Dunn_PhD/Modelling/Med/Combined")
df <- list.files(path="./", full.names = TRUE) %>% 
  lapply(read_csv) %>% 
  bind_rows
df <- as.data.frame(df)
head(df)
mean(df$distance_m)
with(df, std.error(distance_m))
h <- hist(df$distance_m, breaks = 100)
h

Oct <- read.csv("/Volumes/Nick_Dunn_PhD/Modelling/Med/Combined/Complete_October2021.csv")
mean(Oct$distance_m)
max(Dec$distance_m)

#first import all files in a single folder as a list 
rastlist <- list.files(path = "~/opendrift/Med_data/Results/Grid/TIFFS/New_tifs/", pattern='.tif$', all.files=TRUE, full.names=FALSE)
allrasters <- lapply(rastlist, raster)
allrasters <- stack(rastlist)

library(raster)
r_050621 <-'050621.tif' 
r_050621=raster(r_050621)

r_060621 <-'060621.tif' 
r_060621=raster(r_060621)

r_070621 <-'070621.tif' 
r_070621=raster(r_070621)

r_080621 <-'080621.tif' 
r_080621=raster(r_080621)

r_090621 <-'090621.tif' 
r_090621=raster(r_090621)

r_100621 <-'100621.tif' 
r_100621=raster(r_100621)

r_110621 <-'110621.tif' 
r_110621=raster(r_110621)

r_120621 <-'120621.tif' 
r_120621=raster(r_120621)

r_130621 <-'130621.tif' 
r_130621=raster(r_130621)

r_140621 <-'140621.tif' 
r_140621=raster(r_140621)

r_150621 <-'150621.tif' 
r_150621=raster(r_150621)

r_160621 <-'160621.tif' 
r_160621=raster(r_160621)

r_170621 <-'170621.tif' 
r_170621=raster(r_170621)

r_180621 <-'180621.tif' 
r_180621=raster(r_180621)

r_190621 <-'190621.tif' 
r_190621=raster(r_190621)

r_200621 <-'200621.tif' 
r_200621=raster(r_200621)

r_210621 <-'210621.tif' 
r_210621=raster(r_210621)

r_220621 <-'220621.tif' 
r_220621=raster(r_220621)

r_230621 <-'230621.tif' 
r_230621=raster(r_230621)

r_240621 <-'240621.tif' 
r_240621=raster(r_240621)

r_250621 <-'250621.tif' 
r_250621=raster(r_250621)

r_260621 <-'260621.tif' 
r_260621=raster(r_260621)

r_270621 <-'270621.tif' 
r_270621=raster(r_270621)

r_merge <- raster::merge(r_050621,r_060621, r_070621,r_080621, r_090621,r_100621,
                         r_110621,r_120621,r_130621,r_140621,r_150621,r_160621,
                         r_170621,r_180621,r_190621,r_200621,r_210621,r_220621,
                         r_230621,r_240621,r_250621,r_260621,r_270621)
plot(r_merge)
writeRaster(r_merge, "~/opendrift/Med_data/Results/Grid/merged_ratsers.grd")



