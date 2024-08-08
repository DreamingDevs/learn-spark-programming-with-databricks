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


def get_df(spark: SparkSession, source_file: str, schema: StructType):
    return spark \
        .read \
        .format("json") \
        .schema(schema) \
        .load(source_file)


def write_df(df: DataFrame, output_dir: str):
    df.write \
        .format("parquet") \
        .partitionBy("release_year") \
        .mode("overwrite") \
        .option("path", output_dir) \
        .save()


if __name__ == "__main__":
    source_movies_file = sys.argv[1]
    output_files_dir = sys.argv[2]
    config_file_path = sys.argv[3]
    print(f"source_movies_file: {source_movies_file}, output_files_dir: {output_files_dir}, config_file_path: {config_file_path}")

    # Logging
    logger = Logger("INFO").getLogger()

    # Create a spark session
    spark = get_spark_session(config_file_path)

    # Define Schema
    movies_schema = get_movies_schema()

    # Read the JSON file into a DataFrame with the defined schema
    movies_df = get_df(spark, source_movies_file, movies_schema)

    movies_df.show(10, truncate=False)
    logger.info(f"Total records of movies dataset: {movies_df.count()}")

    # Repartition based on release_year
    movies_df = movies_df.repartition(20, "release_year")
    logger.info(f"Total partitions of movie dataset: {movies_df.rdd.getNumPartitions()}")

    # Write the DataFrame in parquet format
    write_df(movies_df, f"{output_files_dir}/movies")
