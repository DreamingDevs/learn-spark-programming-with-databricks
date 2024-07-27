from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

if __name__ == "__main__":
    source_file = sys.argv[1]
    output_files_dir = sys.argv[2]
    print(f"source_file: {source_file}, output_files_dir: {output_files_dir}")
    
    # Create a spark session
    spark = SparkSession \
        .builder \
        .appName("HelloWorld") \
        .master("local[2]") \
        .getOrCreate()

    # Define Schema
    schema = StructType([
        StructField("movie_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("genre", StringType(), True),
        StructField("release_year", IntegerType(), True),
        StructField("duration", IntegerType(), True)
    ])

    # Read the JSON file into a DataFrame with the defined schema
    movies_df = spark \
        .read \
        .format("json") \
        .schema(schema) \
        .load(source_file)

    movies_df.show(10, truncate=False)

    # Write the DataFrame in parquet format
    movies_df.write \
        .format("parquet") \
        .mode("overwrite") \
        .option("path", output_files_dir) \
        .save()
