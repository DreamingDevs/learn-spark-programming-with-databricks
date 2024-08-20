from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from lib.config import *
from lib.logger import Logger
import logging
import os


def get_spark_session(config_file_path):
    return SparkSession \
        .builder \
        .config(conf=get_spark_conf(config_file_path)) \
        .enableHiveSupport() \
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


def create_hive_table(spark: SparkSession, table_name: str, parquet_dir: str):
    spark.sql(f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
            movie_id STRING,
            title STRING,
            genre STRING,
            duration INT
        )
        PARTITIONED BY (release_year INT)
        STORED AS PARQUET
        LOCATION '{parquet_dir}'
    """)
    # Optionally, you can load the partitions into the table
    spark.sql(f"MSCK REPAIR TABLE {table_name}")


if __name__ == "__main__":
    source_movies_file = sys.argv[1]
    output_files_dir = sys.argv[2]
    config_file_path = sys.argv[3]
    print(f"source_movies_file: {source_movies_file}, output_files_dir: {
          output_files_dir}, config_file_path: {config_file_path}")

    # Logging
    logger = Logger("INFO").getLogger()

    # Create a spark session
    spark = get_spark_session(config_file_path)

    # Define Schema
    movies_schema = get_movies_schema()

    # Read the JSON file into a DataFrame with the defined schema
    movies_df = get_df(spark, source_movies_file, movies_schema)

    # Write the DataFrame in parquet format
    write_df(movies_df, f"{output_files_dir}/movies")

    # Create the Hive table pointing to the Parquet files
    create_hive_table(spark, "movies", f"{os.path.abspath(output_files_dir)}/movies")

    # Query the Hive table
    result_df = spark.sql("SELECT title, genre, release_year FROM movies WHERE release_year >= 2000")
    result_df.show()
