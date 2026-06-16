# from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName("test").getOrCreate()

# df = spark.read.parquet("bronze/customers/customers.parquet")

# print(df.count())
# df.show(5)

# spark.stop()

import os

print(os.listdir("data"))