
from pyspark.sql.functions import *
from pyspark.sql.types import *

class Clean_SilverDims:
    def __init__(self, df=None):
        self.df = df

    def drop_rescue_data(self, *cols):
        self.df = self.df.drop("_rescued_data")
        return self.df
   
    def read_data(self, folder_name):
        self.df = spark.readStream.format("cloudFiles") \
            .option("cloudFiles.format","parquet") \
            .option("cloudFiles.schemaLocation", f"abfss://silver@jessdatalake.dfs.core.windows.net/{folder_name}/checkpoint_location") \
            .option("schemaEvolutionMode", "addNewColumns") \
            .load(f"abfss://bronze@jessdatalake.dfs.core.windows.net/{folder_name}")
        return self.df
    
    def write_data(self, folder_name, data_name):
        self.df.writeStream.format("delta") \
            .outputMode("append") \
            .option("checkpointLocation", f"abfss://silver@jessdatalake.dfs.core.windows.net/{folder_name}/checkpoint_location") \
            .option("path", f"abfss://silver@jessdatalake.dfs.core.windows.net/{folder_name}/{data_name}") \
            .trigger(once=True) \
            .toTable(f"musicstreaming_project.silver.{data_name}")
        return self.df
    
    def drop_dup(self, primary_key):
        self.df = self.df.dropDuplicates([primary_key])
        return self.df
