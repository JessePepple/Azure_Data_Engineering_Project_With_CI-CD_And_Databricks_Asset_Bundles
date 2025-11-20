import dlt

@dlt.table(
    name= "DimDate_staging"
)
def DimDate_staging():
  df = spark.readStream.table("musicstreaming_project.silver.dimdate")
  return df

dlt.create_streaming_table("DimDate")

dlt.create_auto_cdc_flow(
    target= "DimDate",
    source= "DimDate_staging",
    keys = ["date_key"],
  sequence_by = "date",
  stored_as_scd_type = "2",
  track_history_except_column_list = None,
  name = None,
  once = False
)