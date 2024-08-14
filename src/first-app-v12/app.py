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

    # Give a rank to the movies within a genre in the descending order of duration
    window_spec = Window.partitionBy("genre").orderBy(desc("duration"))
    movies_df = movies_df.withColumn("rank", rank().over(window_spec))
    movies_df.show(100, truncate=False)

    # Incremental cumulative sum of durations within each genre, ordered by duration
    window_spec_cum_sum = Window.partitionBy("genre").orderBy(desc("duration")).rowsBetween(Window.unboundedPreceding, Window.currentRow)
    movies_df = movies_df.withColumn("cumulative_duration", sum("duration").over(window_spec_cum_sum))
    movies_df.show(100, truncate=False)

    # Decremental Total remaining duration within each genre, ordered by duration
    window_spec_remaining_duration = Window.partitionBy("genre").orderBy(desc("duration")).rowsBetween(Window.currentRow, Window.unboundedFollowing)
    movies_df = movies_df.withColumn("remaining_duration", sum("duration").over(window_spec_remaining_duration))
    movies_df.show(100, truncate=False)

    # Total sum of durations within each genre, ordered by duration
    window_spec_cum_sum = Window.partitionBy("genre").orderBy(desc("duration")).rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
    movies_df = movies_df.withColumn("total_duration", sum("duration").over(window_spec_cum_sum))
    movies_df.show(100, truncate=False)

    logger.info(f"Total records of movies dataset: {movies_df.count()}")

    # Write the DataFrame in parquet format
    write_df(movies_df, f"{output_files_dir}/movies")
