# Cloud-Based Big Data Analytics Pipeline (AWS + PySpark)
## Airline Delay Cause Analytics

An end-to-end cloud-based big data analytics pipeline that ingests airline delay data from Amazon S3, processes it using PySpark on EC2, writes curated outputs back to S3 (CSV + Parquet), and runs analytical queries using Spark SQL. The pipeline demonstrates automation, orchestration, and monitoring using AWS Lambda, Systems Manager (SSM), and SNS, and includes downstream analytics via SageMaker Autopilot and Power BI dashboards.

## High-Level Architecture

S3 (raw) → AWS Lambda (trigger) → SSM Run Command → EC2 (PySpark jobs + bash runner) → S3 (processed data + logs) → SNS (email notifications) → Power BI / SageMaker Autopilot

## Key Features

- End-to-end PySpark ETL pipeline  
- Feature engineering and aggregations on airline delay data  
- Spark SQL analytics for insights  
- Automated execution via Lambda + SSM  
- Monitoring and alerting using SNS  
- AutoML experiment with SageMaker Autopilot  
- Interactive dashboards built in Power BI  
- Cloud-native design using IAM roles (no hardcoded credentials)

## Dataset

This project uses the Airline Delay Cause Dataset, which includes flight volumes, cancellations, diversions, delay counts, and delay causes such as Carrier, Weather, NAS, and Late Aircraft. Key columns include year, month, airport, carrier, arr_flights, arr_del15, and multiple delay-cause metrics (counts and minutes).

Note: The full dataset is intentionally excluded from Git to keep the repository lightweight. A small sample dataset (~5k rows) is provided in data/sample/ for local testing.

## Repository Structure

.
├── pipeline/  
│   └── run_pipeline.sh              # End-to-end pipeline runner (EC2)  
├── src/  
│   ├── ingest_airline.py            # Ingest raw data from S3  
│   ├── transform_airline.py         # Cleaning, feature engineering, and aggregations  
│   ├── save_to_s3.py                # Write processed outputs to S3  
│   └── sql_airline.py               # Spark SQL analytics  
├── data/  
│   ├── raw/                         # (gitignored) full dataset location  
│   └── sample/  
│       └── Airline_Delay_Cause_sample.csv  
├── outputs/  
├── processed/                   # (gitignored) example outputs and logs  
├── docs/  
│   └── MiniProject_Report.pdf       # Detailed project report  
├── .gitignore  
├── LICENSE  
└── README.md  

## Quickstart (Local Execution)

Create a virtual environment:

python -m venv .venv  
source .venv/bin/activate  

Install dependencies:

pip install -U pip pyspark  

Run using the sample dataset:

python airline_project/transform_airline.py --input data/sample/Airline_Delay_Cause_sample.csv --output outputs/local  

If scripts are configured for S3 paths, they should be run on EC2 where S3 access is provided via an IAM role.

## Running on AWS (Recommended Setup)

Prerequisites:
- S3 bucket with raw/, processed/, and analytics/logs/ folders  
- EC2 instance with Apache Spark installed  
- EC2 IAM role with S3 and SNS permissions  
- Optional Lambda and SSM for serverless triggering  

Pipeline execution on EC2:

cd /home/ubuntu/Pipeline  
chmod +x run_pipeline.sh  
./run_pipeline.sh  

The pipeline script runs all PySpark jobs in sequence, uploads outputs and logs to S3, and publishes success or failure notifications via SNS.

## AutoML (SageMaker Autopilot)

The processed dataset can be imported into SageMaker Autopilot (Canvas) for a regression task with total delay minutes as the target variable.

## Dashboarding (Power BI)

Power BI is used to build interactive dashboards using processed CSV files stored in S3, including:
- Monthly flight trends
- Airport-level traffic
- Delay cause breakdowns
- Airline reliability insights

## Notes for Reviewers

No AWS secrets are stored in this repository. Access is managed using IAM roles and managed policies. Large datasets and generated outputs are excluded using .gitignore. This project demonstrates real-world cloud data engineering and big data analytics practices.

## License

MIT License
