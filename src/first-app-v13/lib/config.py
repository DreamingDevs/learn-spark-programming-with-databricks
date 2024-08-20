import configparser
from pyspark import SparkConf
import pyarrow


def get_spark_conf(config_file_path):
    conf = SparkConf()
    parser = configparser.ConfigParser()

    parser.read(config_file_path)
    for (key, val) in parser.items("SPARK_APP_CONFIGS"):
        conf.set(key, val)

    return conf
