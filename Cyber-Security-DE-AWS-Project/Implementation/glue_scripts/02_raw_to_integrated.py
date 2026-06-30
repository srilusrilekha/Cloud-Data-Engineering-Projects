"""
AWS Glue Job: Raw Layer to Integrated Layer

Purpose:
- Connect to Amazon Redshift using credentials from AWS Secrets Manager
- Execute stored procedures that transform raw data into integrated business entities
- Apply business rules, standardization, and relationship logic inside Redshift

Note:
This is a generic portfolio sample. Replace placeholders with environment-specific values.
"""

import sys
import json
import boto3
import psycopg2
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
        "redshift_secret_name",
        "raw_schema",
        "integrated_schema",
    ],
)

job_name = args["JOB_NAME"]
environment = args["environment"]
redshift_secret_name = args["redshift_secret_name"]
raw_schema = args["raw_schema"]
integrated_schema = args["integrated_schema"]


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
    """Retrieve Redshift credentials from AWS Secrets Manager."""
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def get_redshift_connection(secret: dict):
    """Create Redshift connection using psycopg2."""
    return psycopg2.connect(
        host=secret["host"],
        port=secret["port"],
        dbname=secret["database"],
        user=secret["username"],
        password=secret["password"],
    )


def execute_stored_procedure(connection, procedure_name: str, parameters: list):
    """Execute a Redshift stored procedure."""
    cursor = connection.cursor()

    placeholders = ", ".join(["%s"] * len(parameters))
    sql = f"CALL {procedure_name}({placeholders});"

    print(f"Executing stored procedure: {procedure_name}")
    cursor.execute(sql, parameters)

    connection.commit()
    cursor.close()

    print(f"Completed stored procedure: {procedure_name}")


# --------------------------------------------------
# Execute Raw to Integrated Transformation
# --------------------------------------------------

print(f"{job_name} started at {datetime.utcnow()}")

redshift_secret = get_secret(redshift_secret_name)
connection = get_redshift_connection(redshift_secret)

try:
    stored_procedures = [
        {
            "name": "<integrated_schema>.<stored_procedure_name>",
            "parameters": [raw_schema, integrated_schema, environment],
        }
    ]

    for procedure in stored_procedures:
        execute_stored_procedure(
            connection,
            procedure["name"].replace("<integrated_schema>", integrated_schema),
            procedure["parameters"],
        )

    print("Raw to Integrated transformation completed successfully.")

except Exception as error:
    connection.rollback()
    print(f"Raw to Integrated transformation failed: {str(error)}")
    raise error

finally:
    connection.close()


# --------------------------------------------------
# Job Completion
# --------------------------------------------------

print(f"{job_name} completed successfully at {datetime.utcnow()}")

job.commit()
