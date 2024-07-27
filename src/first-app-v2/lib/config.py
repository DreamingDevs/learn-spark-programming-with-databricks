import configparser
from pyspark import SparkConf


def get_spark_conf():
    conf = SparkConf()
    parser = configparser.ConfigParser()

    parser.read("spark.conf")
    for (key, val) in parser.items("SPARK_APP_CONFIGS"):
        conf.set(key, val)

    return conf
