import copernicus_marine_client as copernicusmarine
# user: jjenrette
# password: VTsandtiger1!
copernicusmarine.subset(
  dataset_id="METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
  variables=["analysed_sst", "analysis_error"],
  minimum_longitude=-72.34819398832006,
  maximum_longitude=-63.32486704637709,
  minimum_latitude=40.307356006503596,
  maximum_latitude=45.82726932764703,
  start_datetime="2023-05-01T00:00:00",
  end_datetime="2023-11-01T23:59:59",
  output_directory="../data/enviro/cape/",
  output_filename="capecod_sst.nc",
)

# grabs oceanographic data from May 1, 2023 to November 1, 2023