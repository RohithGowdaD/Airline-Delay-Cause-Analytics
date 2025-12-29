import argparse
from pyspark.sql import SparkSession

def parse_args():
    p = argparse.ArgumentParser(description="Ingest airline delay dataset with PySpark.")
    p.add_argument("--input", default="data/raw/Airline_Delay_Cause.csv", help="Input CSV path (local or s3a://...)")
    p.add_argument("--show", type=int, default=10, help="Number of rows to display")
    return p.parse_args()

def main():
    args = parse_args()
    spark = SparkSession.builder.appName("Airline Delay Ingest").getOrCreate()

    df = (spark.read.option("header", True)
                    .option("inferSchema", True)
                    .csv(args.input))

    print("Number of rows:", df.count())
    print("Schema:")
    df.printSchema()
    df.show(args.show, truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
