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
library(ggplot2)
#data(wrld_simpl)
#rast <-raster()
#res(rast)=0.1
###
#ChagosEEZ  <- readOGR(dsn="~/Desktop/PhD/Mapping folder/Chagos_shapefiles",layer="ChagosEEZ")
#####
######create empty plot
#PB <-extent(71.0,72.8,-6,-4.5)
#PB <-crop(ChagosEEZ,PB)
#raster::plot(PB)

#set working directory
setwd("/Volumes/Nick_Dunn_PhD/Modelling/Med/Oct2021")
### reading in the files in the folder
EXP_files <- list.files("./", pattern = ".nc")
head(EXP_files)

for(i in 1:59){
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
hist(complete_df$distance_m, xlab = "Distance (m)",ylab = "Number of particles",
     main = "June 2021", breaks = 50)
min(complete_df$distance_m)
max(complete_df$distance_m)
mean(complete_df$distance_m)
with(complete_df, std.error(distance_m))
apply(complete_df, 2, sd)
write.csv(complete_df, "../Complete_June2021.csv", row.names = FALSE)


setwd("/Volumes/Nick_Dunn_PhD/Modelling/Med")
April_all <- read.csv("./Combined/Complete_April2021.csv")
April_all$Month <- 4
complete_df$month <- 8
head(complete_df)
p <- ggplot(complete_df, aes(x = month, y = distance_m)) +
  geom_violin()
p + stat_summary(fun=mean, geom="point", shape=23, size=2) + 
  geom_boxplot(width=0.1)

October_all <- read.csv("./Combined/Complete_October2021.csv")
Feb_all <- read.csv("./Combined/Complete_February2022.csv")

head(April_all)
mean(October_all$distance_m)
std.error(October_all$distance_m)/1000

mean(Feb_all$distance_m)
std.error(Feb_all$distance_m)/1000


