## What is Spark?

Spark is an open-source framework that is used for distributed data processing. In other words, it can be considered a successor to the Hadoop platform. Spark provides a unified interface to process large volumes of data by abstracting the complexity of distributed computing and storage.

Historically, Hadoop solved the problem of variety, volume, and velocity of data by adopting distributed mechanisms for cluster management (YARN), storage mechanism (HDFS), and compute (MapReduce). However, Hadoop-based systems are not optimized for performance and have strong coupling with YARN and Java. Spark was designed to solve some native issues encountered in the Hadoop system.

1. Spark supports in-memory processing, hence optimized for performance.
2. Spark programming supports Java, Scala, Python, and R.
3. Cluster management is available through Kubernetes, Mesos, and YARN orchestrators.
4. Spark supports advanced data workloads such as ML algorithms, graph and stream processing through MLlib, GraphX, and Stream API.
5. Spark eases the development of data applications through a unified API of Dataframe and Spark SQL through the adoption of Resilient Distributed Dataset (RDD).

Following is the high-level logical architecture of Spark.

![Spark logical architecture](./../images/spark-basics.png)

Following are key aspects of different layers in the architecture:
1. The top layer exposes APIs for addressing different data processing requirements like machine learning, graph, stream and SQL. Using these APIs, we can build continuous and streaming data workloads.
2. The Spark Core is the foundation for the top layer through its Resilient Distributed Dataset (RDD), optimizations (catalyst optimizer), scheduling, and other abstractions.
3. The Spark engine is the heavy lifter that understands the Spark application request, generates DAG, breaks the flow into smaller units, schedules the units, supplies the required data to the units, monitors and provides fault tolerance to the smaller units, and finally orchestrates the results.
4. Cluster manager provides the abstraction of master and worker nodes of the cluster from the Spark application. Typically, this layer would be substituted by YARN, Mesos, and Kubernetes.
5. Compute and storage resources power all the layers with required processing and storage space. This layer is provisioned by cloud infrastructure providers like Azure, AWS, and GCP.

## What is Databricks

Databricks is a Spark-based managed cloud data platform that provides comprehensive solutions related to data engineering, data science, data analytics, and machine learning. Following are key features of Databricks when compared with Spark.

1. Databricks provides managed Spark environments, which simplify the configuration, setup, and management of Spark clusters.
2. It provides notebooks and workspaces for the team's collaboration, making it easy to develop and deploy data processing and analysis tasks.
3. It provides data governance through the Unity Catalog.
4. Databricks offers lakehouse capabilities through Delta Lake.
5. There are administrative controls and automations available in Databricks for managing large-scale projects.
6. Built-in security controls are available to provide role-based access controls.
7. Data ingestion and integration is made easy through Delta Live tables and Autoloader.
8. Photon acceleration is available to deliver optimized performance in SQL analytical workloads.
9. Different features available for Data science and ML flows

## Read and Write formats

Spark supports a variety of read and write formats. Here are some of the most commonly used formats and their characteristics:


| Format  | Format         | Schema evolution | Suitable for                              | Optimized for Large <br/>and complex data? |
|---------|----------------|------------------|-------------------------------------------|--------------------------------------------|
| TEXT    | Row            | Hard             | Log processing, <br/>Simple data exchange | No                                         |
| JSON    | Nested         | Hard             | Web and APIs                              | No                                         |
| CSV     | Row            | Hard             | Simple data exchange                      | No                                         |
| PARQUET | Columnar       | Easy             | Analytical queries                        | Yes                                        |
| ORC     | Columnar       | Easy             | Analytical queries                        | Yes                                        |
| AVRO    | Row            | Easy             | Batch & Streaming Data                    | Yes                                        |
| DELTA   | Columnar       | Easy             | Batch & Streaming Data                    | Yes                                        |
| HUDI    | Row & Columnar | Easy             | Batch & Streaming Data                    | Yes                                        |

## Spark Lazy evaluation with transformations and actions

Let's first understand Spark's transformations and actions. Transformations are operations on existing Spark DataFrame to produce new DataFrame. Examples are `select`, `selectExpr`, `filter`, `where`, `grouoBy`, `agg`, `join`, and `withColumn`, etc. Actions are operations which execute all the transformations and return the result to the drive program. Example actions are `show`, `collect`, `write`, `count`.

Transformations are lazy, they don't trigger the execution, whereas actions trigger the execution. Spark creates an execution plan in the form of a DAG (Directed Acyclic Graph) based on transformations, which is then optimized to reduce data shuffle and operations. Finally, the DAG is executed when an action is encountered. This is called lazy evaluation in Spark.

