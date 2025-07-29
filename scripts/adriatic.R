# Load necessary libraries
library(rnaturalearth)
library(rnaturalearthdata)
library(ncdf4)
library(ggplot2)
library(dplyr)
library(sf)
library(ggmap)
library(tidyr)
library(scales)

setwd("~/Dropbox/eDNA/particle-abundance/scripts/")

# Function to extract and reshape particle coordinates from .nc file
extract_and_reshape_particle_coords <- function(nc_file) {
  nc_data <- nc_open(nc_file)
  
  # Extract variables
  lon <- ncvar_get(nc_data, "lon")
  lat <- ncvar_get(nc_data, "lat")
  time <- ncvar_get(nc_data, "time")
  degraded <- ncvar_get(nc_data, "degraded")
  
  # Extract time units and convert time to POSIXct
  # time_units <- ncatt_get(nc_data, "time", "units")$value
  # time_origin <- sub(".*since ", "", time_units)
  # time <- as.POSIXct(time_origin, tz = "UTC") + time * 3600  # Assuming time is in hours
  
  # Reshape data so that each row is a particle at a specific time step
  num_particles <- ncol(lon)
  num_time_steps <- nrow(lon)
  
  df <- data.frame(
    lon = as.vector(t(lon)),
    lat = as.vector(t(lat)),
    time = as.vector(t(time)),
    # particle_id = rep(1:num_particles, times = num_time_steps),
    degraded = as.vector(t(degraded))
  )
  
  nc_close(nc_data)
  return(df)
}

# Path to the directory with .nc files
output_path <- "../data/output/adriatic2024/"
nc_files <- list.files(output_path, pattern = "\\.nc$", full.names = TRUE)

# Extract and combine coordinates from all .nc files
all_coords <- lapply(nc_files, extract_and_reshape_particle_coords)
all_coords_df <- bind_rows(all_coords)

# Filter out degraded particles and those not at the specific time
all_coords_df <- all_coords_df %>%
  filter(degraded == 0, time == time[length(unique(time))])

# Load world map data
world <- ne_countries(scale = "medium", returnclass = "sf")

# Coordinates for Vlore, Albania and Venice, Italy
vlore_coords <- c(lon = 19.4876, lat = 40.4662)
venice_coords <- c(lon = 12.3155, lat = 45.4408)

transect = c(lon = 12.3155, lat = 44.3)

# Distances in kilometers from Vlore
distances_km <- c(110, 165, 220, 275, 465, 520, 575, 630)

# Calculate the intermediate points at the specified distances
intermediate_points <- geosphere::destPoint(p = vlore_coords, b = geosphere::bearing(vlore_coords, transect), d = distances_km * 1000)  # Convert km to meters
# Append the specific coordinates
additional_point <- data.frame(lon = 12.95, lat = 44.65)
intermediate_points <- rbind(intermediate_points, additional_point)
# Convert the intermediate points to a data frame for plotting
intermediate_points_df <- as.data.frame(intermediate_points)
colnames(intermediate_points_df) <- c("lon", "lat")
intermediate_points_df$label <- paste0("Station ", 1:nrow(intermediate_points_df))

# Create data frames for Vlore and Venice with labels
vlore_label <- data.frame(lon = vlore_coords["lon"], lat = vlore_coords["lat"], label = "Vlore, Albania")
venice_label <- data.frame(lon = venice_coords["lon"], lat = venice_coords["lat"], label = "Venice, Italy")

# Combine all labels into one data frame
all_labels_df <- bind_rows(intermediate_points_df, vlore_label, venice_label)

# Plot the binned density of particles on the world map with colored landmasses, blue water, labeled points, and an arrow on the segment line
bin_plot = ggplot() +
  stat_bin2d(data = all_coords_df, aes(x = lon, y = lat), bins = 16) +  # Adjust bins as needed
  scale_fill_viridis_c() +
  geom_segment(aes(x = vlore_coords["lon"], y = vlore_coords["lat"], xend = venice_coords["lon"], yend = venice_coords["lat"]),
               color = "black", size = 1, arrow = arrow(type = "closed", length = unit(0.3, "cm"))) +
  geom_sf(data = world, fill = "lightgray", color = "black") +
  geom_point(data = intermediate_points_df, aes(x = lon, y = lat), color = "red", size = 2) +
  geom_point(data = vlore_label, aes(x = lon, y = lat), color = "blue", size = 3) +
  geom_point(data = venice_label, aes(x = lon, y = lat), color = "blue", size = 3) +
  geom_text(data = all_labels_df, aes(x = lon, y = lat, label = label), vjust = -1.25, color = "black") +
  theme_minimal() +
  labs(title = "Simulated Relative Density of eDNA in the Adriatic Sea (May 26-28, 2024)",
       x = "Longitude", y = "Latitude",
       fill = "eDNA Particles") +
  coord_sf(xlim = c(11.872007936314006, 19.798491021424145), ylim = c(40.1747017584095, 45.865043973178935)) +
  theme(panel.background = element_rect(fill = "lightblue", color = NA),
        panel.grid.major = element_line(color = "grey80", size = 0.5))

smooth_plot = ggplot() +
  stat_density_2d(data = all_coords_df, aes(x = lon, y = lat, fill = ..level..), geom = "polygon", contour = TRUE) +
  scale_fill_viridis_c(option="viridis") +  
  geom_sf(data = world, fill = "lightgray", color = "black") +
  geom_point(data = intermediate_points_df, aes(x = lon, y = lat), color = "black", size = 2) +
  geom_point(data = vlore_label, aes(x = lon, y = lat), color = "blue", size = 3) +
  geom_point(data = venice_label, aes(x = lon, y = lat), color = "blue", size = 3) +
  geom_text(data = all_labels_df, aes(x = lon, y = lat, label = label), vjust = -1.25, color = "black") +
  theme_minimal() +
  labs(title = "eDNA Abundance in the Adriatic Sea (May 27-29, 2024)",
       x = "Longitude", y = "Latitude",
       fill = "eDNA Density Factor") +
  coord_sf(xlim = c(11.872007936314006, 19.798491021424145), ylim = c(40.1747017584095, 45.865043973178935)) +
  theme(panel.background = element_rect(fill = "white", color = NA),
        panel.grid.major = element_line(color = "grey80", size = 0.5))
smooth_plot

# Save the plot
ggsave(filename = "../figures/adriatic2024.png", plot = smooth_plot, width = 10, height = 8, dpi = 300)

