import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def parse_args():
    p = argparse.ArgumentParser(description="Clean + feature engineer airline delay data with PySpark.")
    p.add_argument("--input", default="data/raw/Airline_Delay_Cause.csv", help="Input CSV path (local or s3a://...)")
    p.add_argument("--output", default="outputs/local", help="Output folder for curated files")
    return p.parse_args()

def main():
    args = parse_args()
    spark = SparkSession.builder.appName("Airline Transform").getOrCreate()

    df = (spark.read.option("header", True)
                    .option("inferSchema", True)
                    .csv(args.input))

    # Basic cleaning
    df = df.dropna()

    # Feature engineering
    df = df.withColumn(
        "total_delay_minutes",
        col("carrier_delay") +
        col("weather_delay") +
        col("nas_delay") +
        col("security_delay") +
        col("late_aircraft_delay")
    )

    df = df.withColumn(
        "total_delay_count",
        col("carrier_ct") +
        col("weather_ct") +
        col("nas_ct") +
        col("security_ct") +
        col("late_aircraft_ct")
    )

    # Save curated outputs
    out_parquet = f"{args.output}/airline_processed_parquet"
    out_csv = f"{args.output}/airline_processed_csv"
    (df.write.mode("overwrite").parquet(out_parquet))
    (df.write.mode("overwrite").option("header", True).csv(out_csv))

    print("Saved:")
    print(" -", out_parquet)
    print(" -", out_csv)

    spark.stop()

if __name__ == "__main__":
    main()
