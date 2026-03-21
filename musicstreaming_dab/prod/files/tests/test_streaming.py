import sys
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from unittest.mock import patch, MagicMock


sys.path.append(
    "/Workspace/Users/jessepepple36@gmail.com/Azure_Data_Engineering_Project_With_CI-CD_And_Databricks_Asset_Bundles/musicstreaming_dab/prod/files/utils"
)

from utilities import Clean_SilverDims  


# ---------------------------
# Spark fixture (Databricks-safe)
# ---------------------------
@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.getActiveSession()
    if spark is None:
        spark = SparkSession.builder.getOrCreate()
    return spark


# ---------------------------
# drop_rescue_data
# ---------------------------
def test_drop_rescue_data(spark):
    data = [("Alice", 1), ("Bob", 2)]
    df = spark.createDataFrame(data, ["name", "_rescued_data"])

    transformer = Clean_SilverDims(df)
    result = transformer.drop_rescue_data()

    assert "_rescued_data" not in result.columns
    assert "name" in result.columns


# ---------------------------
# drop_dup
# ---------------------------
def test_drop_dup(spark):
    data = [("Alice", 1), ("Alice", 1), ("Bob", 2)]
    df = spark.createDataFrame(data, ["name", "id"])

    transformer = Clean_SilverDims(df)
    result = transformer.drop_dup("name")

    # Only 2 unique names should remain
    assert result.count() == 2
    assert "name" in result.columns
    assert "id" in result.columns



        
  

