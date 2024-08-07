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

def apply_transformations(df: DataFrame):
    return df.where(ratings_df.rating_id == 999987)


if __name__ == "__main__":
    source_ratings_file = sys.argv[1]
    output_files_dir = sys.argv[2]
    config_file_path = sys.argv[3]
    print(f"source_ratings_file: {source_ratings_file}, output_files_dir: {output_files_dir}, config_file_path: {config_file_path}")

    # Logging
    logger = Logger("INFO").getLogger()

    # Create a spark session
    spark = get_spark_session(config_file_path)
    
    # Settings to make sure cache is not cached
    spark.conf.set("spark.sql.adaptive.enabled", "false")
    spark.catalog.clearCache()

    # Define Schema
    ratings_schema = get_ratings_schema()

    # Read the JSON file into a DataFrame with the defined schema
    ratings_df = get_df(spark, source_ratings_file, ratings_schema)

    # repartition the ratings_df to simulate multiple partitions
    partitioned_df = ratings_df.repartition(2)

    # apply transformations
    filtered_df = apply_transformations(partitioned_df)

    logger.info(filtered_df.collect())