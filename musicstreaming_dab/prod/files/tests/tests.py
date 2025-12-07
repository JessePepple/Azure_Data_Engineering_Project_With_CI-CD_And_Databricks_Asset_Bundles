import pytest
from unittest.mock import MagicMock
from Clean_SilverDims import Clean_SilverDims


@pytest.fixture
def spark_mock():
    spark = MagicMock()
    reader = spark.readStream.format.return_value
    reader.option.return_value = reader
    reader.load.return_value = MagicMock()
    writer = MagicMock()
    writer.option.return_value = writer
    writer.trigger.return_value = writer
    spark.readStream = MagicMock(format=MagicMock(return_value=reader))
    spark.DataFrameWriter = MagicMock
    return spark


def test_read_data(spark_mock, monkeypatch):
    monkeypatch.setattr("Clean_SilverDims.spark", spark_mock)
    c = Clean_SilverDims()
    df = c.read_data("DimArtist")
    assert df is not None


def test_drop_dup():
    df_mock = MagicMock()
    df_mock.dropDuplicates.return_value = "clean_df"
    c = Clean_SilverDims(df_mock)
    result = c.drop_dup("artist_id")
    assert result == "clean_df"


def test_drop_rescue_data():
    df_mock = MagicMock()
    df_mock.drop.return_value = "clean_df"
    c = Clean_SilverDims(df_mock)
    result = c.drop_rescue_data("_rescued_data")
    assert result == "clean_df"


def test_write_data(spark_mock, monkeypatch):
    df_mock = MagicMock()
    writer = df_mock.writeStream.format.return_value
    writer.outputMode.return_value = writer
    writer.option.return_value = writer
    writer.trigger.return_value = writer

    monkeypatch.setattr("Clean_SilverDims.spark", spark_mock)

    c = Clean_SilverDims(df_mock)
    result = c.write_data("DimArtist", "dimartist")
    assert result == df_mock
