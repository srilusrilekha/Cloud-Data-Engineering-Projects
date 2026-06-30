"""
AWS Glue Job: Integrated Layer to Linked Layer

Purpose:
- Connect to Amazon Redshift using credentials from AWS Secrets Manager
- Execute stored procedures that generate reporting-ready metric tables
- Populate the Linked Layer (vw_metrics,vw_master_metrics) used by downstream analytics and Power BI dashboards

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


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "environment",
        "redshift_secret_name",
        "integrated_schema",
        "linked_schema",
    ],
)

job_name = args["JOB_NAME"]
environment = args["environment"]
redshift_secret_name = args["redshift_secret_name"]
integrated_schema = args["integrated_schema"]
linked_schema = args["linked_schema"]


sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(job_name, args)


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


print(f"{job_name} started at {datetime.utcnow()}")

redshift_secret = get_secret(redshift_secret_name)
connection = get_redshift_connection(redshift_secret)

try:
    stored_procedures = [
        {
            "name": "<linked_schema>.sp_load_vm_master_metrics",
            "parameters": [integrated_schema, linked_schema, environment],
        },
        {
            "name": "<linked_schema>.sp_load_vm_metrics",
            "parameters": [integrated_schema, linked_schema, environment],
        },
    ]

    for procedure in stored_procedures:
        execute_stored_procedure(
            connection,
            procedure["name"].replace("<linked_schema>", linked_schema),
            procedure["parameters"],
        )

    print("Integrated to Linked transformation completed successfully.")
    print("Linked Layer tables populated: VM_master_metrics, VM_metrics")

except Exception as error:
    connection.rollback()
    print(f"Integrated to Linked transformation failed: {str(error)}")
    raise error

finally:
    connection.close()


print(f"{job_name} completed successfully at {datetime.utcnow()}")

job.commit()
