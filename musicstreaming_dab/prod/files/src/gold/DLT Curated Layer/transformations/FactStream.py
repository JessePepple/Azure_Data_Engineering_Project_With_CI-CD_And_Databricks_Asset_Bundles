import dlt

@dlt.table(
    name= "FactStream_staging"
)
def FactStream_staging():
  df = spark.readStream.table("musicstreaming_project.silver.factstream")
  return df

dlt.create_streaming_table("FactStream")

dlt.create_auto_cdc_flow(
    target= "FactStream",
    source= "FactStream_staging",
    keys = ["stream_id"],
  sequence_by = "stream_timestamp",
  stored_as_scd_type = "1",
  track_history_except_column_list = None,
  name = None,
  once = False
)