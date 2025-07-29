import copernicusmarine as cm
# user: jjenrette
# password: VTsandtiger1!
cm.subset(
  dataset_id="cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m",
  variables=["uo", "vo"],
  minimum_longitude=11.872007936314006,
  maximum_longitude=19.798491021424145,
  minimum_latitude=40.1747017584095,
  maximum_latitude=45.865043973178935,
  start_datetime="2024-05-25T00:00:00",
  end_datetime="2024-05-29T00:00:00",
  minimum_depth=0.49402499198913574,
  maximum_depth=34.43415069580078,
  output_directory="./tmp/",
  output_filename="adriatic-cur.nc"
)