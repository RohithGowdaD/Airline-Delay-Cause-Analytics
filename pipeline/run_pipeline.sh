#!/usr/bin/env bash
set -euo pipefail

# ====== Runtime config (override via env) ======
: "${AWS_DEFAULT_REGION:=us-east-1}"
: "${JAVA_HOME:=/usr/lib/jvm/java-17-openjdk-amd64}"
: "${SPARK_HOME:=/opt/spark}"
: "${SPARK_SUBMIT:=$SPARK_HOME/bin/spark-submit}"

: "${BUCKET:=rg422-bigdata}"
: "${RAW_KEY:=raw/Airline_Delay_Cause.csv}"

: "${PROCESSED_PREFIX:=processed}"
: "${ANALYTICS_PREFIX:=analytics}"
: "${LOGS_PREFIX:=logs}"

# SNS topic ARN (optional)
: "${TOPIC_ARN:=}"

export AWS_DEFAULT_REGION JAVA_HOME
export PATH="$JAVA_HOME/bin:$SPARK_HOME/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# ====== Paths ======
PIPELINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$PIPELINE_DIR/../airline_project" && pwd)"

TS="$(date +"%Y-%m-%d_%H-%M-%S")"
LOG_DIR="$HOME/pipeline/logs"
mkdir -p "$LOG_DIR"
LOG_LOCAL="$LOG_DIR/pipeline_$TS.log"

S3_LOG_PATH="s3://$BUCKET/$PROCESSED_PREFIX/$ANALYTICS_PREFIX/$LOGS_PREFIX/pipeline_$TS.log"
S3_RAW_PATH="s3a://$BUCKET/$RAW_KEY"
S3_OUT_PATH="s3a://$BUCKET/$PROCESSED_PREFIX"

{
  echo "=========================================="
  echo "Airline PySpark Pipeline"
  echo "Timestamp : $TS"
  echo "Bucket    : $BUCKET"
  echo "Raw       : $S3_RAW_PATH"
  echo "Output    : $S3_OUT_PATH"
  echo "=========================================="

  echo "[1/3] Ingest (schema + sample)"
  "$SPARK_SUBMIT" "$PROJECT_DIR/ingest_airline.py" --input "$S3_RAW_PATH" --show 5

  echo "[2/3] Transform + write curated outputs (CSV + Parquet)"
  "$SPARK_SUBMIT" "$PROJECT_DIR/transform_airline.py" --input "$S3_RAW_PATH" --output "$S3_OUT_PATH"

  echo "[3/3] Run Spark SQL analytics"
  "$SPARK_SUBMIT" "$PROJECT_DIR/sql_airline.py" --input "$S3_RAW_PATH"

  echo "=========================================="
  echo "Pipeline finished OK"
  echo "=========================================="
} | tee "$LOG_LOCAL"

# Upload logs to S3 (best effort)
if command -v aws >/dev/null 2>&1; then
  aws s3 cp "$LOG_LOCAL" "$S3_LOG_PATH" || true
fi

# Optional SNS notification (best effort)
if [[ -n "$TOPIC_ARN" ]] && command -v aws >/dev/null 2>&1; then
  aws sns publish --topic-arn "$TOPIC_ARN" --subject "✅ Pipeline Succeeded"         --message "Airline pipeline succeeded at $TS. Log: $S3_LOG_PATH" || true
fi
