## First Application

Update the [requirements.txt](./../src/requirements.txt) by adding pyspark dependency.

> NOTE: Make sure
> 1. The PySpark package version matches with the Spark version installed on local machine.
> 2. The Virtual env. is activated.

Create [app.py](./../src/first-app-v1/app.py) which reads the `movies.json` file and writes in `parquet` format.

Details of the code:
1. A `SparkSession` has been created which is configured to run on local cores. The session can be configured with remote cluster as well, which we will try out later.
2. It is always good practice to define the schema and read the source data.
3. The final output is written to the directory in the parquet format.

```
cd learn-spark-programming-with-databricks
cd src
pip install -r requirements.txt
cd first-app-v1
python3 app.py ../../dataset/movies.json ../../dataset/output
```

![First Application](../images/first-app-v1.png)


## Handling Spark Configuration

Spark framework allows us to configure application with multiple options to optimize the performance and manage the resources efficiently. Following are few important configuration options.

1. `spark.app.name`
2. `spark.master`
3. `spark.executor.memory`
4. `spark.executor.cores`
5. `spark.executor.memoryOverhead`
6. `spark.driver.memory`
7. `spark.driver.cores`
8. `spark.driver.memoryOverhead`
9. `spark.default.parallelism`
10. `spark.sql.shuffle.partitions`
11. `spark.sql.autoBroadcastJoinThreshold`
12. `spark.sql.codegen.wholeStage`
13. `spark.eventLog.enabled`
14. `spark.eventLog.dir`
15. `spark.checkpoint.dir`
16. `spark.checkpoint.compress`

> NOTE: Spark comes with default configuration template which can be typically found at `<SPARK_HOME>/conf/spark-defaults.conf.template`. We can rename it to `spark-default.conf` to make it effective.

Create [app.py](./../src/first-app-v2/app.py) which extends V1 version. All the configuration settings are placed in [spark.conf](./../src/first-app-v2/spark.conf) which is read by [lib/config.py](./../src/first-app-v2/lib/config.py). The `SparkConf` object is the applied to the `SparkSession`.

> NOTE: Make sure the virtual env. is activated.

```
cd learn-spark-programming-with-databricks
cd src
pip install -r requirements.txt
cd first-app-v2
python3 app.py ../../dataset/movies.json ../../dataset/output spark.conf
```

## Creating a custom logger

Let's now create a custom logger to log messages from the spark application. The custom logger class is based on Python's logging package which uses `StreamHandler` to stream logs to the sink. The `CustomLogger` code can be found at [lib/logger.py](./../src/first-app-v3/lib/logger.py) and is then used in [app.py](./../src/first-app-v3/app.py).

> NOTE: Make sure the virtual env. is activated.

```
cd learn-spark-programming-with-databricks
cd src
pip install -r requirements.txt
cd first-app-v3
python3 app.py ../../dataset/movies.json ../../dataset/output spark.conf
```

![First Application V3](../images/first-app-v3.png)

## Deploy the spark application

To make the `lib` as a package, we need to add [lib/\_\_init\_\_.py](./../src/first-app-v4/lib/__init__.py).

Update the [spark.conf](./../src/first-app-v4/spark.conf) with the master url.
```
spark.master=spark://Ramis-MacBook-Pro.local:7077
```

> NOTE: Make sure the virtual env. is activated.

Execute below commands to run our application standalone cluster.

```
cd learn-spark-programming-with-databricks/src/first-app-v4/
zip -r lib.zip lib/*
cd ../..
mkdir temp
cd temp
mv ../src/first-app-v4/lib.zip .
cp ../src/first-app-v4/app.py .
cp ../src/first-app-v4/spark.conf .
cp ../dataset/movies.json .
```

The above commands creates the `lib` zip package, copies the `lib.zip`, `app.py`, `spark.conf` and `movies.json` to temp directory.

Submit the spark application from temp directory by executing below command. Replace the `--master` url with the master url of your local's standalone cluster.

```
spark-submit --master spark://Ramis-MacBook-Pro.local:7077 --py-files lib.zip app.py movies.json output spark.conf
```
![First Application V4](../images/first-app-v4.png)

At the end of execution, we can delete the `temp` folder.

```
cd learn-spark-programming-with-databricks
rm -rf temp
```

## Package Spark Application dependencies

Sometimes our Spark app will be having dependencies from different packages (like pyarrow, pandas, matplotlib etc.). These packages will not be available readily in spark env. Let's see how we can package the dependencies of our Spark application. 

Let's create a fake dependency by importing pyarrow in [lib/config.py](./../src/first-app-v5/lib/config.py). Include pyarrow and venv-pack in the [requirements.txt](./../src/requirements.txt).

> NOTE: Make sure the virtual env. is activated.

```
cd learn-spark-programming-with-databricks
cd src
pip install -r requirements.txt
cd ..
venv-pack -o venv.tar.gz

cd src/first-app-v5/
zip -r lib.zip lib/*
cd ../..
mkdir temp
cd temp
mv ../src/first-app-v5/lib.zip .
cp ../src/first-app-v5/app.py .
cp ../src/first-app-v5/spark.conf .
cp ../dataset/movies.json .
mv ../venv.tar.gz .
```

Submit the spark application from temp directory by executing below command. We pass the packages virtual environment through `--archives` attribute. The `#env` tells the spark-submit command where to unzip the virtual env.

We also need to set `PYSPARK_DRIVER_PYTHON` and `PYSPARK_PYTHON` to leverage the python executable from the unzipped virtual env. on the cluster. Replace the `--master` url with the master url of your local's standalone cluster.

```
export PYSPARK_DRIVER_PYTHON=python3
export PYSPARK_PYTHON=./env/bin/python3
spark-submit --master spark://Ramis-MacBook-Pro.local:7077 --archives venv.tar.gz#env --py-files lib.zip app.py movies.json output spark.conf
```

![First Application V5](../images/first-app-v5.png)

At the end of execution, we can delete the `temp` folder.

```
cd learn-spark-programming-with-databricks
rm -rf temp
```

## Unit testing Spark Application

Update [requirements.txt](../src/requirements.txt) with `pytest` dependency.

The [app.py](../src/first-app-v6/app.py) code is refactored to be modular. This way we can mock different functions which would make the overall code more unit test friendly.

Add [\_\_init\_\_.py](../src/first-app-v6/__init__.py) to `first-app-v6` directory to convert it to a module, so that we can import the entire module in unit tests. Add `first-app-v6` module to `PYTHONPATH` by executing below command (change the path accordingly to you local path).

```
export PYTHONPATH=$PYTHONPATH:/Users/ramivemula/projects/learn-spark-programming-with-databricks/src/first-app-v6
```

Create test cases at [test_app.py](../src/tests-v6/test_app.py). Execute the test cases by following command.

```
cd learn-spark-programming-with-databricks
pytest src/tests-v6/
```

![Unit tests](../images/unit-tests.png)

## Basic Spark Transformations

PySpark provides a variety of transformations that can be applied to DataFrames and RDDs. However, RDD based programming is not encouraged by the Spark community because of following advantages of DataFrame APIs. Spark DataFrame is `immutable` which means any transformation will lead to a new DataFrame instance.

1. Abstractions are user-friendly and expressive
2. Wide range of built-in functions 
3. Catalyst optimizations (Column pruning, predicate pushdown etc.)
4. Ease of usage
5. Interoperability with SQL

Following are basic transformations which are available in Spark. Code can be found out at [app.py](../src/first-app-v7/app.py).

> NOTE: We will discuss aggregate and join based transformations in subsequent sections. This section only covers basic transformations.

| Transformation      | Details                                                                       |
|---------------------|-------------------------------------------------------------------------------|
| select() / alias()  | Projects a set of expressions and returns a new DataFrame.                    |
| selectExpr()        | Uses SQL expression to project the data                                       | 
| filter() / where()  | Filters rows using a given condition. Filter uses SQL expression.             |
| withColumn()        | Adds a new column or replaces an existing column.                             |
| drop()              | Drops a column from the DataFrame.                                            |
| withColumnRenamed() | Renames a given column name                                                   |
| orderBy() / sort()  | Returns a new DataFrame sorted by the specified columns.                      |
| distinct()          | Returns a new DataFrame with distinct rows.                                   |
| udf()               | User Defined Function (UDF) is used to implement custom logic on a DataFramer |

## Joins in Spark Application

Spark supports following joins.

1. inner: Returns only the rows that have matching values in both DataFrames.
2. outer: Returns all rows from both DataFrames irrespective whether there are matching or not.
3. left_outer: Returns all rows from the left DataFrame and the matched rows from the right DataFrame.
4. right_outer: Returns all rows from the right DataFrame and the matched rows from the left DataFrame.
5. left_semi: Returns only the rows from the left DataFrame for which there is a match in the right DataFrame.
6. left_anti: Returns only the rows from the left DataFrame for which there is no match in the right DataFrame.
7. crossJoin: Returns the Cartesian product of the two DataFrames.

`inner` join implementation of `movies` and `ratings` datasets can be found at [app.py](../src/first-app-v8/app.py).

Following are key aspects of spark joins.

1. Make sure column names are unique between the datasets.
2. Ensure the columns of join condition have same schema.
3. Avoid cartesian product joins, which means make sure the join condition is not broad.

> NOTE: There are performance optimization strategies which can be applied to improve join performance. We will discuss them in subsequent sections.

![spark-join](../images/spark-join.png)

## Aggregates in Spark Application

Following are few types of aggregates which are support by spark - `avg, count, sum, min, max, stddev, variance, approximate_count_distinct, first, last`

Aggregates implementation of `movies` and `ratings` datasets can be found at [app.py](../src/first-app-v9/app.py).

![spark-join](../images/spark-aggregates.png)

## Narrow and Wide dependency in Spark Application

Narrow and wide dependencies in Spark is about how data will be shuffled across the Spark cluster when certain transformations are applied to produce results.

| Dependency | Description                                                                                                                                                                                                  | Examples                           | 
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| Narrow     | Any transformation operation which can be performed on the data of a single partition to provide the results. These operations are faster because there is no additional work for spark to shuffle the data. | `select`, `filter`, `where`, `map` |
| Wide       | Any transformation operation which needs data from multiple partitions to provide the results. These operations are slow due to data shuffle operations.                                                     | `groupBy`, `join`, `orderBy`       |

Spark engine creates an execution plan of the Spark application in the form of a DAG - Directed Acyclic Graph. A DAG is combination of multiple jobs, where each job is further divided into stages. Spark will execute multiple tasks under each stage.

The execution plan is optimized to ensure minimal reshuffling of data and combine multiple operations to remove redundant processing. We can view the generated DAG by going to the Spark's history server.

> NOTE: Refer to `Enable Spark History Server` section for details on how to setup history server. In my case, the history server is running at `http://192.168.0.184:18080/`.

> NOTE: Below executions are ran by using spark-submit command. For more details, please refer to previous sections.

Lets' first submit a simple Spark application which just reads the `ratings.json` file and performs a `collect` action. Remember that the DAG will be executed only on performing a Spark action. Take the reference of [app-v1.py](../src/first-app-v10/app-v1.py). We can clearly see that there is only one job with one stage which is reading JSON. Also note that there are no shuffle operations (from the table shown in below image).

![Spark DAG 1](../images/spark-dag-1.png)

Now let's update the code to `repartition` the dataframe and see how the DAG changes. Take the reference of [app-v2-py](../src/first-app-v10/app-v2.py). The DAG shows we have one job with two stages. The first stage is to read the json file, repartition and write to exchange. The second stage is to read from exchange and collect the data.

The DAG shows that the json file has been processed and as part of `reparition` operation the data was made available at `exchange` (shuffle write operation). Finally, when we use `collect`, the shuffle read operation came in from exchange.

![Spark DAG 2](../images/spark-dag-2.png)

Now lets update the code by applying few transformations. We are going to apply `where`, `groupBy` and `agg` transformations as referred in [app-v3-py](../src/first-app-v10/app-v3.py). The DAG shows we have one job, but with 3 stages. The first stage holds the same responsibility as mentioned previously. The second stage where the shuffle read operation (because of `groupBy` transformation) happens, transformations get applied and shuffle write operation to write the output to exchange. The final stage will read the data from exchange as part of collect operation.

![Spark DAG 3](../images/spark-dag-3.png)

The details of individual stage can be viewed by clicking on the respective stage. The below image shows the DAG and details of Stage 2 from above execution. We can clearly see that this stage read 99648 records from exchange, applied transformations and finally wrote back 19931 records to exchange.

![Spark Stage DAG 4](../images/spark-stage-dag-4.png)

The final execution we do is by removing `groupBy` and `agg` transformations and only having `where` transformation. 

We can clearly see that the shuffle write and read operations are reduced when compared with previous execution. This is because `where` is a narrow dependency transformation, whereas `groupBy` and `agg` are wide dependency transformations.

![Spark DAG 5](../images/spark-dag-5.png)

## Partitioning and Bucketing in Spark Application

**Repartition**: It is a method to increase or decrease the number of partitions in a DataFrame (in-memory partitions of executors). This requires a full shuffle of data and can improve the performance by improving the scope for parallelism. We can use `repartition` methods to create partitions.

`repartition` takes `numPartitions` and `cols` as parameters. To give an example, we can create 20 partitions of movies dataset and use `release_year` as the column which will decide on which records can be placed under which partition. Example code can be found out at [app.py](../src/first-app-v11/app.py).

```
movies_df = movies_df.repartition(20, "release_year")
```

> NOTE: Identification of partition keys is important, typically they should be the columns on which aggregates are operated.
> If the cardinality of partition key (example - release_year) is high, we end up in skewed partitions which will impact performance.
> The default spread of partitions happen based on `spark.default.parallelism` configuration. 
 
**PartitionBy**: It is the technique used during the write operation to organize the data in the physical file system based on specified partition key. This technique is usually used to optimize the read operations during queries. This organization of data is not going to impact the repartition of the data across executors. Example code can be found out at [app.py](../src/first-app-v11/app.py).

```
df.write \
    .format("parquet") \
    .partitionBy("release_year") \
    .mode("overwrite") \
    .option("path", output_dir) \
    .save()
```

**Bucketing**: It is the process of organizing data into physical buckets. Unlike `partitionBy` which creates file directories based on partition key, `bucketBy` will create fixed files and store data to respective files by computing hash of the partition key. This will improve the performance of queries as there would be no need to traverse a larger storage. We can use `bucketBy` to create buckets. 

```
def write_df(df: DataFrame, output_dir: str):
    df.write \
        .format("parquet") \
        .bucketBy("release_year") \
        .mode("overwrite") \
        .option("path", output_dir) \
        .save()
```

![Partitions](../images/partitions.png)

As we can see the log message says that we have 20 partition (caused by `reparition`). We can also see the physical data is segregated by release_year (due to `partitionBy`).

![Partitions](../images/partitions-1.png)

## Windowing functions in Spark Application

Spark windowing functions are used to perform calculations across a set of rows that are related to the current row. These functions are particularly useful we want to perform operations such as running totals, moving averages, rankings etc., over a "window" of data.

A window specification contains following -
- **Partitioning**: Divides the dataset into partitions to which the window function is applied independently.
- **Ordering**: Specifies the order of rows within each partition.
- **Frame**: Defines a sliding window of rows around the current row, based on the order.

The implementation of windowing functions can be found at [app.py](../src/first-app-v12/app.py).

We can give rank to the movies in a partition as shown below.

```
# Give a rank to the movies within a genre in the descending order of duration
window_spec = Window.partitionBy("genre").orderBy(desc("duration"))
movies_df = movies_df.withColumn("rank", rank().over(window_spec))
```

The sliding window can be of below formations based on `Window.unboundedPreceding`, `Window.currentRow` and `Window.unboundedFollowing`.
```
# Incremental cumulative sum of durations within each genre, ordered by duration
window_spec_cum_sum = Window.partitionBy("genre").orderBy(desc("duration")).rowsBetween(Window.unboundedPreceding, Window.currentRow)
movies_df = movies_df.withColumn("cumulative_duration", sum("duration").over(window_spec_cum_sum))
```
Window.unboundedPreceding starts from the first row in the partition. Window.currentRow ends at the current row. The sum function accumulates the duration values from the first row of the partition to the current row as shown below.

![Window Functions 1](../images/window-functions-1.png)

```
# Decremental Total remaining duration within each genre, ordered by duration
window_spec_remaining_duration = Window.partitionBy("genre").orderBy(desc("duration")).rowsBetween(Window.currentRow, Window.unboundedFollowing)
movies_df = movies_df.withColumn("remaining_duration", sum("duration").over(window_spec_remaining_duration))
```
Window.currentRow starts at the current row. Window.unboundedFollowing ends at the last row in the partition. The sum function calculates the total duration from the current row to the end of the partition.

![Window Functions 2](../images/window-functions-2.png)

```
# Total sum of durations within each genre, ordered by duration
window_spec_cum_sum = Window.partitionBy("genre").orderBy(desc("duration")).rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
movies_df = movies_df.withColumn("total_duration", sum("duration").over(window_spec_cum_sum))
```

![Window Functions 3](../images/window-functions-3.png)


## Spark SQL with In-memory Hive metastore

The Hive Metastore in Spark acts as a central repository to store metadata for tables, databases, and other data entities that can be queried using SQL. It helps in -

- Storing the table schemas, column types, and data locations. 
- Helps in data cataloging and SQL querying capabilities.
- Partition based query optimizations
- Support schema evolution
- Integration with persistent relational database like MySQL, PostgreSQL, Derby for storing the metadata.

> NOTE: We can submit SQL queries for execution on Spark cluster using Thrift Server interface.

We can configure our local standalone cluster's Hive metastore with persistent databases like MySQL etc. However, for this learning exercise, we are going to configure it using In-memory store.

Firstly, enable Hive support.
```
def get_spark_session(config_file_path):
    return SparkSession \
        .builder \
        .config(conf=get_spark_conf(config_file_path)) \
        .enableHiveSupport() \
        .getOrCreate()
```

Configure the SparkSession to use in-memory hive metastore with the directory (to store managed tables) and derby database (in-memory) classes which are required to support Spark SQL. The complete configuration can be found at [aprk.conf](./../src/first-app-v14/spark.conf).

```
spark.sql.catalogImplementation=in-memory
spark.sql.warehouse.dir=/tmp/spark-warehouse
spark.sql.hive.metastore.sharedPrefixes=org.apache.derby
```

Create an external table pointing to the parquet files directory. We can also use `saveAsTable` method to write the DataFrame as a managed Hive table (for example `df.write.mode("overwrite").format("parquet").partitionBy("release_year").saveAsTable(table_name)`).

```
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
```

Execute the Spark SQL queries. The completed code can be found at [app.py](./../src/first-app-v14/app.py).

```
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
```

When we execute the program, we get below output. Similarly, we can use other regular SQL commands to execute.

> NOTE: The derby in-memory hive metastore creates folders (`metastore_db`) and files (`derby.log`) in current working directory. Add these folders and files to .gitignore.

![Spark SQL](./../images/spark-sql.png)

## Caching in Spark application

Caching in Spark application is the process of storing the Spark SQL table / DataFrame data in-memory (or on disk) to avoid repeated computation and improve the performance of the application. This technique is helpful when the same DataFrame is access multiple times across multiple transformations in the same application.

Below code can be found at [app.py](./../src/first-app-v15/app.py) and related configuration [spark.conf](./../src/first-app-v15/spark.conf).

#### Caching a DataFrame
```
# Cache the ratings_df
ratings_cache_df = ratings_df.cache() # Default is StorageLevel.MEMORY_AND_DISK_DESER

# Alternative way to cache by specifying the storage mechanism
ratings_cache_df = ratings_df.persist(storagelevel.StorageLevel.MEMORY_ONLY)

# Clear ratings Dataframe cache
ratings_cache_df.unpersist()
```

> NOTE: Available storage levels are - NONE, DISK_ONLY, DISK_ONLY_2, DISK_ONLY_3, MEMORY_ONLY, MEMORY_ONLY_2, MEMORY_AND_DISK, MEMORY_AND_DISK_2, OFF_HEAP, MEMORY_AND_DISK_DESER. These options are useful to control the storage mechanism between memory, disk and off-heap. This setting also controls the replication and serialization of cache. 

#### Caching a SQL Table
```
# Cache the movies SQL table
cache_query = spark.sql("CACHE Table movies OPTIONS ('storageLevel' 'MEMORY_ONLY');")

# Read from cached table
movies_cache_df = spark.sql("SELECT title, genre, release_year FROM movies WHERE release_year >= 2000")

# Clear the movies SQL cache
spark.sql("uncache table movies")   
```

> NOTE: To remove all items from the cache, we can use `spark.sql("clear cache")` or `spark.catalog.clearCache()`. 
>
> We can also use catalog methods to cache like `spark.catalog.cacheTable(table_name)` and `spark.catalog.uncacheTable("database.table_name")`.

Some settings which can be tuned to get optimized caching are described as follows.

```
# the number of rows that will be stored in a batch in the columnar cache.
spark.conf.set("spark.sql.inMemoryColumnarStorage.batchSize", "5000")

# whether the in-memory columnar storage should be compressed
spark.conf.set("spark.sql.inMemoryColumnarStorage.compressed", "true")

# Specifies the serializer for Cache
spark.conf.set("spark.sql.cache.serializer", "org.apache.spark.serializer.KryoSerializer")

# the fraction of the JVM heap that is used for Spark's execution and storage memory
spark.conf.set("spark.memory.fraction", "0.7")

# the fraction of spark.memory.fraction that is allocated to storage (caching) versus execution memory.
spark.conf.set("spark.memory.storageFraction", "0.6")
```

Once we execute the app, we can inspect the DAG visualization where we can see the im-memory table and in-memory DataFrame is being used for computation.

![Spark Cache](./../images/cache.png)

![Spark Cache](./../images/cache-1.png)

## Deploy and test the Spark application

In this section we will see how to deploy Spark application to a Databricks cluster and test it. Hope you already created an Azure account as demonstrated [here](./setup_dev_machine.md#azure-and-databricks-setup).

**Step 1**: Login to Azure account and create a Premium Databricks cluster. We can find the `Launch Workspace` option on the created Databricks service, click on it and navigate to the workspace.

![Databricks Cluster](./../images/databricks-1.png)

![Databricks Workspace](./../images/databricks-2.png)

**Step 2**: Navigate to settings and enable DBFS filesystem explorer at Databricks workspace.

![DBFS Workspace](./../images/databricks-3.png)

**Step 3**: Under `catalog` tab, select `Browse DBFS`. Create `firstapp` folder and upload `movies.json` to DBFS. The path of the file is `dbfs:/FileStore/firstapp/movies.json`.

![Upload movies.json](./../images/databricks-4.png)

**Step 4**: Create compute resource by navigating to `compute` tab. As this cluster is only for testing purpose, we will create a shared cluster with minimum configuration as shown below.

![Create compute](./../images/databricks-7.png)

**Step 5**: The source code can be found at [first-app-v16](./../src/first-app-v16). Package the application by executing below commands, make sure the contents of the zip file have the same hierarchy (when we un-zip, the folder should contain `__init__.py, app.py, spark.conf, lib/__init__.py, lib/config.py, lib/logger.py`).

> NOTE: The code has been simplified because the purpose of this section to demonstrate the execution of app in Databricks environment.

```
cd learn-spark-programming-with-databricks/src/
zip -r first-app-v16.zip first-app-v16/
```

**Step 6**: Under workspace tab, create a folder with name `first-app`. Right click the folder and import the package to the `first-app` folder.

![Upload package](./../images/databricks-5.png)

**Step 7**: Under workspace tab, create a new notebook with name `first-app-notebook` under `first-app` folder.

![New Notebook](./../images/databricks-6.png)

**Step 8**: Execute the below code.

```
import sys
import os

# Define the directory containing app.py and lib
app_directory = '/Workspace/first-app/first-app-v16'

# Add this directory to the system path
sys.path.insert(0, app_directory)

# Now import the main function from app.py
from app import main

# Define the paths
movies_path = 'dbfs:/FileStore/firstapp/movies.json'
output_path = 'dbfs:/FileStore/firstapp/output'
config_path = 'first-app-v16/spark.conf'

# Call the main function
main(movies_path, output_path, config_path)
```

We can see below output.

![Output](./../images/databricks-8.png)

**Step 9**: Ensure to clean up all the resources.

- Delete first-app folder (right click -> move to trash)
- Stop the cluster and delete it
- Delete the DBFS files using `dbutils.fs.rm` command from a notebook (or) manually delete the files
- Delete the firstapp Databricks workspace from the Azure portal
- Ensure all resources groups are also deleted, if not, then delete them manually
