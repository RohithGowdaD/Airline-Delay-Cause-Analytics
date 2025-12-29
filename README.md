# Cloud-Based Big Data Analytics Pipeline (AWS + PySpark) — Airline Delay Cause Dataset

An end-to-end big data analytics pipeline that ingests airline delay data from **Amazon S3**, processes it using **PySpark on EC2**, writes curated outputs back to S3 (**CSV + Parquet**), runs analytics via **Spark SQL**, and demonstrates **automation and monitoring** using **AWS Lambda**, **Systems Manager (SSM)**, and **SNS**.  
The project also includes an **AutoML experiment with SageMaker Autopilot** and an **interactive dashboard built in Power BI**.

---

## Architecture (High Level)

S3 (raw) → Lambda trigger → SSM Run Command → EC2 (PySpark jobs + bash runner) → S3 (processed + logs) → SNS (email notifications) → Power BI dataset refresh

---

## What This Repository Contains

- **PySpark ETL pipeline** for ingestion, cleaning, feature engineering, aggregation, and export
- **Spark SQL analytics** queries
- **Automation script** to run the pipeline end-to-end and upload logs to S3
- **Sample dataset (~5k rows)** for quick local testing
- **Detailed project report (PDF)** describing architecture, implementation, and results

---

## Dataset

This project uses the **Airline Delay Cause Dataset**, which includes flight volumes, cancellations, diversions, and delay causes across multiple years (e.g., **Carrier**, **Weather**, **NAS**, **Late Aircraft**).

Key columns include:
`year`, `month`, `airport`, `carrier`, `arr_flights`, `arr_del15`, and delay-cause metrics (counts and minutes).

> **Note:**  
> The full dataset is intentionally excluded from Git to keep the repository lightweight.  
> Use the sample file in `data/sample/` or download the original dataset and place it under `data/raw/`.

---

## Repository Structure

```text
.
├── pipeline/
│   └── run_pipeline.sh              # End-to-end pipeline runner (EC2)
├── src/
│   ├── ingest_airline.py            # Read raw data from S3
│   ├── transform_airline.py         # Cleaning, feature engineering, and aggregations
│   ├── save_to_s3.py                # Write processed outputs to S3
│   └── sql_airline.py               # Spark SQL analytics
├── data/
│   ├── raw/                         # (gitignored) full dataset location
│   └── sample/
│       └── Airline_Delay_Cause_sample.csv
├── outputs/                         # (gitignored)
├── docs/
│   └── MiniProject_Report.pdf       # Detailed project report
├── .gitignore
├── LICENSE
└── README.md

## Quickstart (Local Execution)

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -U pip pyspark

# Run using the sample dataset
python src/transform_airline.py \
  --input data/sample/Airline_Delay_Cause_sample.csv \
  --output outputs/local
If scripts are configured for S3 paths, they should be run on EC2 where S3 access is provided via an IAM role.

Running on AWS (Recommended)
Prerequisites
S3 bucket with raw/, processed/, and analytics/logs/ folders

EC2 instance with Apache Spark installed

EC2 IAM role with permission to read/write S3 and publish to SNS

Optional Lambda + SSM for serverless triggering

Pipeline Execution (EC2)
bash
Copy code
cd /home/ubuntu/pipeline
chmod +x run_pipeline.sh
./run_pipeline.sh
The pipeline script runs all PySpark jobs sequentially, uploads processed outputs and logs to S3, and publishes success or failure notifications via SNS.

AutoML (SageMaker Autopilot)
The processed dataset can be imported into SageMaker Autopilot (Canvas) for a regression task where the target variable is total delay minutes.

Dashboard (Power BI)
Power BI is used to build interactive dashboards by reading processed CSV files from S3, including:

Monthly flight trends

Airport-level traffic analysis

Delay cause breakdowns

Airline reliability insights

Notes for Reviewers
No AWS secrets are stored in this repository

AWS access is managed using IAM roles and managed policies

Large datasets and generated outputs are excluded using .gitignore

This project demonstrates real-world cloud data engineering and big data analytics practices

License
MIT License

yaml
Copy code

