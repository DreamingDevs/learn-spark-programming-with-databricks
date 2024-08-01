from unittest.mock import patch
from pyspark.sql import *
from pyspark import SparkConf
from app import get_spark_session, get_movies_schema, get_movies_df, write_movies_df
import json
import os
import pytest
import shutil


@pytest.fixture(scope="session")
def mock_spark_session():
    return SparkSession.builder \
        .config(conf=mock_spark_conf("")) \
        .getOrCreate()


def mock_spark_conf(config_file_path):
    conf = SparkConf()
    conf.set("spark.app.name", "TestSpark")
    conf.set("spark.master", "local[2]")
    return conf


def create_test_data():
    test_data = [{"movie_id": 1, "title": "Nice whose.", "genre": "Action", "release_year": 1987, "duration": 83}, {
        "movie_id": 2, "title": "Behind culture.", "genre": "Horror", "release_year": 2020, "duration": 109}]
    test_data_file = "src/tests-v6/test_movies.json"
    with open(test_data_file, 'w') as outfile:
        json.dump(test_data, outfile)

    return test_data_file


def tear_test_data(path: str, is_dir: bool = False):
    if not os.path.exists(path):
        return

    if is_dir:
        shutil.rmtree(path)
    else:
        os.remove(path)


@patch("app.get_spark_conf", side_effect=mock_spark_conf)
def test_get_spark_session(mock_spark_conf):
    session = get_spark_session("")
    assert session.conf.get("spark.app.name") == "TestSpark"


def test_get_movies_schema():
    schema = get_movies_schema()
    assert schema is not None
    assert len(schema.fields) == 5


def test_get_movies_df(mock_spark_session):
    schema = get_movies_schema()
    test_data_file = create_test_data()

    movies_df = get_movies_df(mock_spark_session, test_data_file, schema)

    assert movies_df.count() == 2
    assert movies_df.schema == schema

    movies = movies_df.collect()

    assert movies[0]["movie_id"] == "1"
    assert movies[0]["title"] == "Nice whose."
    assert movies[0]["genre"] == "Action"
    assert movies[0]["release_year"] == 1987
    assert movies[0]["duration"] == 83

    tear_test_data(test_data_file)


def test_write_movies_df(mock_spark_session):
    test_data_file = create_test_data()
    df = mock_spark_session.read.format("json").schema(
        get_movies_schema()).load(test_data_file)
    output_dir = "src/tests-v6/output"
    write_movies_df(df, output_dir)

    assert os.path.exists(output_dir)
    assert os.path.isdir(output_dir)

    tear_test_data(test_data_file)
    tear_test_data(output_dir, True)
