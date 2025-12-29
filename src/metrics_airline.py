from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, desc

spark = SparkSession.builder.appName("Airline Metrics").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True) \
    .csv("data/Airline_Delay_Cause.csv") \
    .dropna()

df = df.withColumn(
    "total_delay_minutes",
    df.carrier_delay + df.weather_delay + df.nas_delay +
    df.security_delay + df.late_aircraft_delay
)

# Metric 1: Total delay by carrier
m1 = df.groupBy("carrier_name").agg(
    sum("total_delay_minutes").alias("total_delay")
).orderBy(desc("total_delay"))

# Metric 2: Average delay by airport
m2 = df.groupBy("airport_name").agg(
    avg("total_delay_minutes").alias("avg_delay")
).orderBy(desc("avg_delay"))

# Metric 3: Yearly delay trend
m3 = df.groupBy("year").agg(
    sum("total_delay_minutes").alias("yearly_delay")
).orderBy("year")

# Metric 4: Monthly delay trend
m4 = df.groupBy("month").agg(
    sum("total_delay_minutes").alias("monthly_delay")
).orderBy("month")

# Metric 5: Average delay by carrier
m5 = df.groupBy("carrier_name").agg(
    avg("total_delay_minutes").alias("avg_carrier_delay")
).orderBy(desc("avg_carrier_delay"))

m1.show(10, False)
m2.show(10, False)
m3.show(10, False)
m4.show(10, False)
m5.show(10, False)

spark.stop()
