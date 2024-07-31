import pytest
from unittest.mock import patch
from pyspark.sql import *
from pyspark import SparkConf
from app import get_spark_session, get_movies_schema

def mock_spark_conf(config_file_path):
    conf = SparkConf()
    conf.set("spark.app.name", "TestSpark")
    conf.set("spark.master", "local[2]")
    return conf

@patch("app.get_spark_conf", side_effect=mock_spark_conf)
def test_get_spark_session(mock_spark_conf):
    session = get_spark_session("")
    assert session.conf.get("spark.app.name") == "TestSpark"

def test_get_movies_schema():
    schema = get_movies_schema()
    assert schema is not None
    assert len(schema.fields) == 5