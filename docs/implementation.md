## First Application

Update the [requirements.txt](./../src/requirements.txt) by adding pyspark dependency.

> NOTE: Make sure
> 1. The PySpark package version matches with the Spark version installed on local machine.
> 2. The Virtual env. is activated.

Create [app.py](./../src/first-app/app.py) which reads the `movies.json` file and writes in `parquet` format.

Details of the code:
1. A `SparkSession` has been created which is configured to run on local cores. The session can be configured with remote cluster as well, which we will try out later.
2. It is always good practice to define the schema and read the source data.
3. The final output is written to the directory in the parquet format.

```
cd learn-spark-programming-with-databricks
pip install -r src/requirements.txt
python3 src/first-app/app.py
```

![First Application](../images/spark-first-app.png)