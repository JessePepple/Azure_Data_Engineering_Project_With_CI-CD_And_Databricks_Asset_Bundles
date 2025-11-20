import dlt 
expectations = {
    "rule 1" : "track_id IS NOT NULL",
    "rule 2" : "track_name IS NOT NULL",
}
@dlt.table(
    name = "dimtrack_staging",
    comment= "Our staging table for the curated dimtrack"
)
def dimtrack_staging():
    df = spark.readStream.table("musicstreaming_project.silver.dimtrack")
    return df
    

dlt.create_streaming_table(name="DimTrack",
expect_all_or_drop= expectations)

dlt.create_auto_cdc_flow(
    target= "DimTrack",
    source= "dimtrack_staging",
    keys= ["track_id"],
    sequence_by= "updated_at",
    stored_as_scd_type= "2",
    track_history_except_column_list = None,
   name = None,
   once = False
)