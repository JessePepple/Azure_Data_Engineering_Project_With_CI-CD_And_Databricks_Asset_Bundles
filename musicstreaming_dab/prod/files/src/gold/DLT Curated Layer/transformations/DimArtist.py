import dlt
expectations = {
    "rule 1" : "artist_id IS NOT NULL",
    "rule 2" : "artist_name IS NOT NULL",
}

@dlt.table(
    name= "DimArtist_staging"
)

def DimArtist_staging():
  df = spark.readStream.table("musicstreaming_project.silver.dimartist")
  return df

dlt.create_streaming_table(
    name= "DimArtist",
    expect_all_or_drop = expectations)

dlt.create_auto_cdc_flow(
    target= "DimArtist",
    source= "DimArtist_staging",
    keys = ["artist_id"],
  sequence_by = "updated_at",
  stored_as_scd_type = "2",
  track_history_except_column_list = None,
  name = None,
  once = False
)