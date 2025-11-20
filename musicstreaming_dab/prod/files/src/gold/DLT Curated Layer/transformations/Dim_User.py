import dlt

@dlt.table(
    name = "DimUser_staging",
    comment = "This is the staging layer for our curated DimUser table"
)
def DimUser_staging():
    df = spark.readStream.table("musicstreaming_project.silver.dimuser")
    return df

dlt.create_streaming_table(
    name = "DimUser")

dlt.create_auto_cdc_flow(
    target = "DimUser",
    source = "DimUser_staging",
    keys = ["user_id"],
  sequence_by = "updated_at",
  stored_as_scd_type = "2",
  track_history_except_column_list = None,
  name = None,
  once = False
)
