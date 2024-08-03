from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from lib.config import *
from lib.logger import Logger
import logging


def get_spark_session(config_file_path):
    return SparkSession \
        .builder \
        .config(conf=get_spark_conf(config_file_path)) \
        .getOrCreate()


def get_movies_schema():
    return StructType([
        StructField("movie_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("genre", StringType(), True),
        StructField("release_year", IntegerType(), True),
        StructField("duration", IntegerType(), True)
    ])


def get_movies_df(spark: SparkSession, source_file: str, schema: StructType):
    return spark \
        .read \
        .format("json") \
        .schema(schema) \
        .load(source_file)


def write_movies_df(df: DataFrame, output_dir: str):
    df.write \
        .format("parquet") \
        .mode("overwrite") \
        .option("path", output_dir) \
        .save()

def apply_movie_transformations(df: DataFrame):
    # SELECT / SELECTEXPR
    df = df.select(col("movie_id").alias("id"), "title", "release_year", "genre", "duration")
    df = df.selectExpr("id", "title", "release_year", "genre", "duration", "CASE WHEN (release_year % 4 = 0 AND release_year % 100 != 0) OR (release_year % 400 = 0) THEN true ELSE false END AS is_leap_year")

    # WHERE / FILTER
    df = df.where(movies_df.duration < 120)
    df = df.filter("duration < 90")

    # WITHCOLUMN
    df = df.withColumn("movie_title", regexp_replace('title', r'[.]', ''))

    # DROP
    df = df.drop("title", "is_leap_year")

    # WITHCOLUMNRENAMED
    df = df.withColumnRenamed("movie_title", "title")

    # ORDERBY
    df = df.orderBy(["release_year", "duration"], ascending=False)

    # DISTINCT
    df.select("genre").distinct().show(truncate=False)

    return df


if __name__ == "__main__":
    source_file = sys.argv[1]
    output_files_dir = sys.argv[2]
    config_file_path = sys.argv[3]
    print(f"source_file: {source_file}, output_files_dir: {
          output_files_dir}, config_file_path: {config_file_path}")

    # Logging
    logger = Logger("INFO").getLogger()

    # Create a spark session
    spark = get_spark_session(config_file_path)

    # Define Schema
    schema = get_movies_schema()

    # Read the JSON file into a DataFrame with the defined schema
    movies_df = get_movies_df(spark, source_file, schema)

    # Apply transformations
    movies_df = apply_movie_transformations(movies_df)

    movies_df.show(10, truncate=False)
    logger.info(f"Total records of movies dataset: {movies_df.count()}")

    # Write the DataFrame in parquet format
    write_movies_df(movies_df, output_files_dir)
