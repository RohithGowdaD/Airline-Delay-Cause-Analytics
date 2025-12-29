import argparse
from pyspark.sql import SparkSession

def parse_args():
    p = argparse.ArgumentParser(description="Run Spark SQL analytics on airline delay dataset.")
    p.add_argument("--input", default="data/raw/Airline_Delay_Cause.csv", help="Input CSV path (local or s3a://...)")
    return p.parse_args()

def main():
    args = parse_args()
    spark = SparkSession.builder.appName("Airline SQL").getOrCreate()

    df = (spark.read.option("header", True)
                    .option("inferSchema", True)
                    .csv(args.input)
                    .dropna())

    df.createOrReplaceTempView("airline")

    queries = [
        # 1) Total arrival delay by carrier
        ("Total arrival delay by carrier",
         """SELECT carrier_name, SUM(arr_delay) AS total_arrival_delay
             FROM airline
             GROUP BY carrier_name
             ORDER BY total_arrival_delay DESC"""),

        # 2) Average arrival delay by airport
        ("Average arrival delay by airport",
         """SELECT airport_name, AVG(arr_delay) AS avg_arrival_delay
             FROM airline
             GROUP BY airport_name
             ORDER BY avg_arrival_delay DESC"""),

        # 3) Yearly delay trends
        ("Yearly delay trends",
         """SELECT year, SUM(arr_delay) AS yearly_delay
             FROM airline
             GROUP BY year
             ORDER BY year"""),

        # 4) Monthly delay trends
        ("Monthly delay trends",
         """SELECT month, SUM(arr_delay) AS monthly_delay
             FROM airline
             GROUP BY month
             ORDER BY month"""),

        # 5) Flight record count by carrier
        ("Flight record count by carrier",
         """SELECT carrier_name, COUNT(*) AS records
             FROM airline
             GROUP BY carrier_name
             ORDER BY records DESC"""),
    ]

    for title, q in queries:
        print("\n==============================")
        print(title)
        print("==============================")
        spark.sql(q).show(10, truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
