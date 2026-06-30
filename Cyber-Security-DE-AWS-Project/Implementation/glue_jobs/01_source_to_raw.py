"""
AWS Glue Job: Source to Raw Layer

Purpose:
- Read data from a source database using credentials from AWS Secrets Manager
- Apply basic validation and standardization
- Load the extracted data into Amazon Redshift Raw Layer

Note:
This is a generic portfolio sample. Replace placeholders with environment-specific values.
"""

import sys
import json
import boto3
from datetime import datetime

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


# --------------------------------------------------
# Runtime Arguments
# --------------------------------------------------

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "environment",
        "source_secret_name",
        "redshift_secret_name",
        "target_schema",
        "target_table",
        "TempDir",
    ],
)

job_name = args["JOB_NAME"]
environment = args["environment"]
source_secret_name = args["source_secret_name"]
redshift_secret_name = args["redshift_secret_name"]
target_schema = args["target_schema"]
target_table = args["target_table"]
temp_dir = args["TempDir"]


# --------------------------------------------------
# Initialize Spark / Glue Context
# --------------------------------------------------

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(job_name, args)


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def get_secret(secret_name: str) -> dict:
    """Retrieve secret value from AWS Secrets Manager."""
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def build_jdbc_url(secret: dict, database_type: str) -> str:
    """Build JDBC URL for source or Redshift connection."""
    host = secret["host"]
    port = secret["port"]
    database = secret["database"]

    if database_type.lower() == "oracle":
        return f"jdbc:oracle:thin:@//{host}:{port}/{database}"

    if database_type.lower() == "redshift":
        return f"jdbc:redshift://{host}:{port}/{database}"

    raise ValueError("Unsupported database type")

def standardize_columns(dataframe):
    """Convert column names to lowercase and replace spaces with underscores."""
    for column in dataframe.columns:
        dataframe = dataframe.withColumnRenamed(
            column,
            column.strip().lower().replace(" ", "_")
        )
    return dataframe

def validate_dataframe(dataframe):
    """Basic validation to ensure data is available before loading."""
    record_count = dataframe.count()

    if record_count == 0:
        raise ValueError("Source query returned zero records.")

    print(f"Validation successful. Record count: {record_count}")
    return record_count


# --------------------------------------------------
# Extract Data from Source
# --------------------------------------------------

print(f"{job_name} started at {datetime.utcnow()}")

source_secret = get_secret(source_secret_name)
redshift_secret = get_secret(redshift_secret_name)

source_jdbc_url = build_jdbc_url(source_secret, "oracle")
redshift_jdbc_url = build_jdbc_url(redshift_secret, "redshift")

source_query = """
SELECT *
FROM <source_schema>.<source_table>
WHERE <incremental_column> >= CURRENT_DATE - 1
"""

source_df = (
    spark.read.format("jdbc")
    .option("url", source_jdbc_url)
    .option("query", source_query)
    .option("user", source_secret["username"])
    .option("password", source_secret["password"])
    .option("driver", "oracle.jdbc.OracleDriver")
    .load()
)

print("Source data extraction completed.")


# --------------------------------------------------
# Transform / Standardize
# --------------------------------------------------

standardized_df = standardize_columns(source_df)
record_count = validate_dataframe(standardized_df)

standardized_df = standardized_df.withColumnRenamed(
    standardized_df.columns[0],
    standardized_df.columns[0]
)

standardized_df.createOrReplaceTempView("source_data")


# --------------------------------------------------
# Load into Redshift Raw Layer
# --------------------------------------------------

target_table_full_name = f"{target_schema}.{target_table}"

(
    standardized_df.write.format("jdbc")
    .option("url", redshift_jdbc_url)
    .option("dbtable", target_table_full_name)
    .option("user", redshift_secret["username"])
    .option("password", redshift_secret["password"])
    .option("driver", "com.amazon.redshift.jdbc.Driver")
    .mode("append")
    .save()
)

print(f"Data loaded into Redshift table: {target_table_full_name}")
print(f"Records loaded: {record_count}")


# --------------------------------------------------
# Job Completion
# --------------------------------------------------

print(f"{job_name} completed successfully at {datetime.utcnow()}")

job.commit()
