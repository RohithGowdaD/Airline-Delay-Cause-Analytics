# Cloud-Based Big Data Analytics Pipeline (AWS + PySpark) — Airline Delay Cause Dataset

End-to-end big data pipeline that ingests airline delay data from **Amazon S3**, processes it with **PySpark on EC2**, writes curated outputs back to S3 (CSV + Parquet), runs analytics via **Spark SQL**, and demonstrates **automation + monitoring** using **AWS Lambda + Systems Manager (SSM) + SNS**. The project also includes an AutoML experiment using **SageMaker Autopilot** and an interactive dashboard built in **Power BI**.

## Architecture (high level)

S3 (raw) → Lambda trigger → SSM Run Command → EC2 (PySpark jobs + bash runner) → S3 (processed + logs) → SNS email notifications → Power BI dataset refresh

## What this repo contains

- **PySpark pipeline** for ingestion, cleaning, feature engineering, aggregations, and export
- **Spark SQL analytics** queries
- **Automation script** to run the pipeline end-to-end and push logs to S3
- **Sample dataset** (5k rows) for quick local testing
- **Project report** (PDF) describing infrastructure, tasks, and results

## Dataset

This project uses the **Airline Delay Cause Dataset**, which includes flight volume, cancellations, and delay causes across multiple years (e.g., carrier / weather / NAS / late aircraft).  
Key columns include `year`, `month`, `airport`, `carrier`, `arr_flights`, `arr_del15`, and delay-cause metrics (counts + minutes).

> Note: The full dataset is not tracked in Git to keep the repo lightweight. Use the sample file in `data/sample/` or download the original dataset and place it under `data/raw/`.

## Repository structure

```text
.
├── Pipeline/
│   └── run_pipeline.sh              # End-to-end runner (EC2)
├── airline_project/
│   ├── ingest_airline.py            # Read raw data from S3
│   ├── transform_airline.py         # Clean + feature engineering + aggregations
│   ├── save_to_s3.py                # Write processed outputs to S3
│   └── sql_airline.py               # Spark SQL analytics
├── data/
│   ├── raw/                         # (ignored) full dataset goes here
│   └── sample/
│       └── Airline_Delay_Cause_sample.csv
├── outputs/
│   └── Processed/                   # Example outputs/logs from runs (ignored by default)
├── docs/
│   └── MiniProject_Report.pdf
└── README.md
```

## Quickstart (local)

### 1) Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip pyspark
```

### 2) Run with the sample dataset (local mode)

```bash
python airline_project/transform_airline.py --input data/sample/Airline_Delay_Cause_sample.csv --output outputs/local
```

> If your scripts currently assume S3 paths, you can add a simple `--input/--output` CLI wrapper, or run them in your EC2 environment where S3 access is configured via IAM role.

## Running on AWS (recommended)

### Prerequisites

- An S3 bucket with folders for `raw/`, `processed/`, and `analytics/logs/`
- An EC2 instance with Spark installed (or use a managed Spark distribution)
- EC2 IAM Role with permission to read/write S3 and publish to SNS
- (Optional) Lambda + SSM for serverless triggering

### Pipeline execution (EC2)

```bash
cd /home/ubuntu/pipeline
chmod +x run_pipeline.sh
./run_pipeline.sh
```

## AutoML (SageMaker Autopilot)

The processed dataset can be imported into SageMaker Autopilot (Canvas) for a regression task where the target is **total delay minutes**.  

## Dashboard (Power BI)

Power BI is used to build interactive visualizations (flight trends, delay causes, reliability, etc.) reading the processed CSV output from S3.

## Notes for reviewers

- **No AWS secrets are stored in this repo.** AWS access is intended via EC2 instance roles and managed policies.
- Large datasets and generated outputs are excluded via `.gitignore`.

## License

MIT (feel free to change).

