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

def get_ratings_schema():
    return StructType([
        StructField("rating_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("movie_id", IntegerType(), True),
        StructField("rating", IntegerType(), True),
        StructField("rating_date", StringType(), True)
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
        .mode("overwrite") \
        .option("path", output_dir) \
        .save()


if __name__ == "__main__":
    source_movies_file = sys.argv[1]
    source_ratings_file = sys.argv[2]
    output_files_dir = sys.argv[3]
    config_file_path = sys.argv[4]
    print(f"source_movies_file: {source_movies_file}, source_ratings_file: {source_ratings_file}, output_files_dir: {output_files_dir}, config_file_path: {config_file_path}")

    # Logging
    logger = Logger("INFO").getLogger()

    # Create a spark session
    spark = get_spark_session(config_file_path)

    # Define Schema
    movies_schema = get_movies_schema()
    ratings_schema = get_ratings_schema()

    # Read the JSON file into a DataFrame with the defined schema
    movies_df = get_df(spark, source_movies_file, movies_schema)
    ratings_df = get_df(spark, source_ratings_file, ratings_schema)

    movies_df.show(10, truncate=False)
    ratings_df.show(10, truncate=False)
    logger.info(f"Total records of movies dataset: {movies_df.count()}, ratings dataset: {ratings_df.count()}")

     # Join movies_df and ratings_df on movie_id
    movie_ratings_df = movies_df.join(ratings_df, movies_df.movie_id == ratings_df.movie_id, how="left_outer").drop(ratings_df.movie_id)

    # ALTERNATIVE
    # movie_ratings_df = movies_df.join(ratings_df, "movie_id", "left_outer")

    # Show the joined DataFrame
    movie_ratings_df.show(10, truncate=False)
    logger.info(f"Total records of movie ratings dataset: {movie_ratings_df.count()}")

    # Write the DataFrame in parquet format
    write_df(movies_df, f"{output_files_dir}/movies")
    write_df(ratings_df, f"{output_files_dir}/ratings")
    write_df(movie_ratings_df, f"{output_files_dir}/movie_ratings")
