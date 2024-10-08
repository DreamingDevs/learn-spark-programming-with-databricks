# Learn Spark Programming with Databricks

Welcome to the "Learn Spark Programming with Databricks" repository! This is your one-stop destination to master Apache Spark and Databricks through a comprehensive, hands-on learning journey.

This repository is designed to guide you step-by-step through the essential concepts and hands-on practices of Apache Spark and Databricks. Below, you’ll find a detailed roadmap of tasks, each carefully curated to build your expertise from the ground up. Whether you're setting up your development environment or diving deep into Spark's powerful features, this table will help you track your progress and stay organized as you advance through the learning journey.

Each task includes a direct link to the corresponding documentation or code samples, making it easy to navigate through the content. Ready to master Spark? Let's get started!

> NOTE: Credit to ChatGPT for transforming my thoughts into write-ups.

| S.No. | Task                                                          | Date       | Status                                     | Details                                                                          |
|-------|---------------------------------------------------------------|------------|--------------------------------------------|----------------------------------------------------------------------------------|
| 1     | What is Spark? How it is different from Hadoop?               | 07-24-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#what-is-spark)                                           |
| 2     | What is Databricks? How it is different from Spark?           | 07-26-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#what-is-databricks)                                      |
| 3     | Spark Architecture and Execution Modes                        | 08-05-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#spark-architecture)                                      |
| 4     | Setup Development environment with Visual Studio Code and Git | 07-22-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/setup_dev_machine.md#development-tools-setup)                      |
| 5     | Install Java, Python and Spark                                | 07-23-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/setup_dev_machine.md#spark-setup)                                  |
| 6     | Create Azure and Databricks accounts                          | 07-25-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/setup_dev_machine.md#azure-and-databricks-setup)                   |
| 7     | Setup the Python virtual env. [Local env.]                    | 07-25-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/setup_dev_machine.md#setup-python-virtual-env)                     |
| 8     | Creating a sample dataset                                     | 07-26-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/dataset.md#create-a-sample-dataset)                                |
| 9     | Create and test the Spark application [Local env.]            | 07-26-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#first-application)                               |
| 10    | Handle Spark Configuration [Local env.]                       | 07-27-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#handling-spark-configuration)                    |
| 11    | Logging in Spark application [Local env.]                     | 07-27-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#creating-a-custom-logger)                        |
| 12    | Start a Spark cluster [Local env.]                            | 07-28-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/setup_dev_machine.md#start-a-spark-cluster)                        |
| 13    | Submit the Spark application to cluster [Local env.]          | 07-28-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#deploy-the-spark-application)                    |
| 14    | Package Spark application dependencies [Local env.]           | 07-29-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#package-spark-application-dependencies)          |
| 15    | Enable Spark History Server [Local env.]                      | 07-30-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/setup_dev_machine.md#enable-spark-history-server)                  |
| 16    | Unit testing of Spark application [Local env.]                | 08-01-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#unit-testing-spark-application)                  |
| 17    | Read & Write formats and modes in Spark application           | 07-31-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#read-and-write-formats-and-modes)                        |
| 18    | Spark Dataframe API transformations                           | 08-02-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#basic-spark-transformations)                     |
| 19    | Spark Joins                                                   | 08-02-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#joins-in-spark-application)                      |
| 20    | Spark Aggregates                                              | 08-05-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#aggregates-in-spark-application)                 |
| 21    | Spark Actions and Transformations                             | 08-07-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#spark-lazy-evaluation-with-transformations-and-actions)  |
| 22    | Understanding Narrow and Wide dependency through DAG          | 08-07-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#narrow-and-wide-dependency-in-spark-application) |
| 23    | Shuffle Sort Merge Join vs Broadcast Join strategies          | 08-20-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#shuffle-sort-merge-join-and-broadcast-join)              |
| 24    | Spark Partitioning and Bucketing                              | 08-09-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#partitioning-and-bucketing-in-spark-application) |
| 25    | Windowing functions in Spark Application                      | 08-13-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#windowing-functions-in-spark-application)        |
| 26    | Spark Performance and partition optimizations                 | 08-22-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#spark-performance-and-partition-optimizations)           |
| 27    | Spark SQL with Hive Metastore                                 | 08-20-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#spark-sql-with-in-memory-hive-metastore)         |
| 28    | Caching in Spark Application                                  | 08-24-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#caching-in-spark-application)                    |
| 29    | Estimation of resources                                       | 08-24-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/basics.md#estimation-of-resources)                                 |
| 30    | Deploy and test the Spark application [Databricks env.]       | 08-25-2024 | ![Completed](./images/icons/completed.png) | [Link](./docs/implementation.md#deploy-and-test-the-spark-application)           |

With this comprehensive list of tasks, we've successfully covered the core fundamentals of Apache Spark. Your journey through Spark’s architecture, transformations, optimizations, and deployments has equipped you with the essential knowledge to build and manage robust Spark applications.

But the journey doesn’t end here! We will soon dive into Spark Streaming, where you’ll learn to process real-time data streams with the same power and efficiency you've mastered with Spark's core functionalities. No breaks, just continuous learning—so stay tuned for the next exciting chapter!

| S.No. | Task                                                                               | Date       | Status                                 | Details |
|-------|------------------------------------------------------------------------------------|------------|----------------------------------------|---------|
| 1     | What is Spark Streaming? What problems does it solve compared to batch processing? | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 2     | What is the streaming execution plan and query flow?                               | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 3     | What are the important APIs for stream processing?                                 | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 4     | What are the different sources and sinks in Spark Streaming?                       | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 5     | Create a streaming application to read data from Kafka and write to a Delta table. | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 6     | What are idempotency issues and how can they be resolved?                          | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 7     | What are Delta tables? Provide examples of Delta tables.                           | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 8     | What are streaming aggregates? How do they differ from incremental aggregates?     | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 9     | What is a state store provider? How does it help Spark Streaming?                  | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 10    | What are stateless and stateful transformations?                                   | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 11    | What are unbounded continuous aggregators and time-bound aggregators?              | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 12    | What are tumbling window and sliding window aggregates?                            | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 13    | What is watermarking, and how does it work with output modes?                      | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 14    | What are stateful and stateless joins? How does watermarking affect joins?         | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 15    | How do you handle CDC (Change Data Capture) updates in streaming applications?     | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |
| 16    | What is the optimized configuration for a streaming application?                   | 09-20-2024 | ![Pending](./images/icons/pending.png) |         |


> [Optional] If you’re interested in customizing your terminal to match the setup used in this guide, you can install iTerm2 and ZSH with the PowerLevel10k theme. Follow the instructions provided [here](./docs/setup_dev_machine.md#terminal-setup).