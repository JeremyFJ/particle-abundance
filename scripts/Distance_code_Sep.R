###Plot points on map
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
library(plotrix)


#set working directory
setwd("/Volumes/Nick_Dunn_PhD/Modelling/Med/Sep2021")
### reading in the files in the folder
EXP_files <- list.files("./", pattern = ".nc")
head(EXP_files)

for(i in 1:90){
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
  final_lon <- sapply(long, function(x) x[max(which(!is.na(x)))])
  lat[lat > 180] <- NA
  lati <- as.data.frame(lat)
  final_lat <- sapply(lati, function(x) x[max(which(!is.na(x)))])
  
  final_location <- cbind(final_lat, final_lon)
  final_location <- as.data.frame(final_location)
  final_location$start_lat <- Start_latitude
  final_location$start_lon <- Start_longitude
  
  # write.csv(final_location, "~/Desktop/PhD/Modelling of eDNA/Results/Location_files/PB_71_7E_5_22S.csv", row.names = F)
  write.csv(final_location, 
            file = paste("final_location", EXP_files[i], ".csv", sep = "_"),
            row.names = FALSE)
  
}

#final locations
#read in all csvs
ldf <- list() # creates a list
listcsv <- dir(pattern = "*.csv") # creates the list of all the csv files in the directory
for (k in 1:length(listcsv)){
  ldf[[k]] <- read.csv(listcsv[k])
}

#
complete_df <- ldf %>%
  bind_rows()

#Distance calculation
head(complete_df)
complete_df$distance_m <- NA
for (i in 1:nrow(complete_df)){
  complete_df[i,]$distance_m <- distGeo(c(complete_df[i,]$start_lon, complete_df[i,]$start_lat),
                                        c(complete_df[i,]$final_lon, complete_df[i,]$final_lat))
}
write.csv(complete_df, "../Complete_September2021.csv", row.names = FALSE)
