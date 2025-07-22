from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum

spark = SparkSession.builder \
        .appName("Most downloaded datasets") \
        .config("spark.jars", "mariadb-java-client-3.5.4.jar") \
        .getOrCreate()

jdbc_url= "jdbc:mariadb://localhost:3306/kaggle"

connection_properties = {
        "user" : "jucky",
        "password": "123",
        "driver" : "org.mariadb.jdbc.Driver"
}

df = spark.read.jdbc(
        url = jdbc_url,
        table = "datasets"
        properties = connection_properties
)

result = df.groupBy("day").agg(
        _sum("downloadCount").alias("total_downloads")
)
